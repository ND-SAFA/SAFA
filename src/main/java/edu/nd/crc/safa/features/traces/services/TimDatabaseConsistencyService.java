package edu.nd.crc.safa.features.traces.services;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;
import java.util.logging.Logger;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.services.ArtifactService;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.ApprovalStatus;
import edu.nd.crc.safa.features.traces.entities.db.TraceMatrixEntry;
import edu.nd.crc.safa.features.traces.entities.db.TraceType;
import edu.nd.crc.safa.features.types.entities.db.ArtifactType;
import edu.nd.crc.safa.features.types.entities.db.ArtifactTypeCount;
import edu.nd.crc.safa.features.types.repositories.ArtifactTypeRepository;
import edu.nd.crc.safa.features.types.services.ArtifactTypeCountService;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.features.versions.repositories.ProjectVersionRepository;

import lombok.AllArgsConstructor;
import org.javatuples.Pair;
import org.springframework.boot.context.event.ApplicationReadyEvent;
import org.springframework.context.event.EventListener;
import org.springframework.stereotype.Service;

/**
 * This service runs a function on startup that ensures all TIM information
 * for all projects is consistent. This shouldn't be needed long-term, but it's
 * the easiest way to add the TIM information to projects that don't have it,
 * which is needed for the initial implementation of the TIM calculations.
 */
@Service
@AllArgsConstructor
public class TimDatabaseConsistencyService {

    private static final Logger logger = Logger.getLogger(TimDatabaseConsistencyService.class.getName());

    private TraceMatrixService traceMatrixService;
    private ArtifactTypeRepository typeRepository;
    private ArtifactTypeCountService artifactTypeCountService;
    private ProjectVersionRepository versionRepository;
    private ArtifactService artifactService;
    private TraceService traceService;

    @EventListener(ApplicationReadyEvent.class)
    public void updateCounts() {
        long startTime = System.currentTimeMillis();

        for (ProjectVersion version : versionRepository.findAll()) {
            List<ArtifactAppEntity> artifacts = artifactService.getAppEntities(version);
            List<TraceAppEntity> traces = traceService.getAppEntities(version, null);

            updateTypes(version, artifacts);
            updateTraces(version, artifacts, traces);
        }

        long endTime = System.currentTimeMillis();

        logger.info("Update TIM information in " + (endTime - startTime) + "ms");
    }

    private void updateTypes(ProjectVersion version, List<ArtifactAppEntity> artifacts) {
        Map<String, ArtifactTypeCount> typeCountMap = new HashMap<>();

        for (ArtifactAppEntity artifact : artifacts) {
            String typeName = artifact.getType();

            if (!typeCountMap.containsKey(typeName)) {
                Optional<ArtifactType> type = typeRepository
                    .findByProjectAndNameIgnoreCase(version.getProject(), typeName);
                ArtifactTypeCount count = artifactTypeCountService.getOrCreate(version, type.orElseThrow());
                count.setCount(0);
                typeCountMap.put(typeName, count);
            }

            ArtifactTypeCount count = typeCountMap.get(typeName);
            count.setCount(count.getCount() + 1);
        }

        for (ArtifactTypeCount count : typeCountMap.values()) {
            artifactTypeCountService.save(count);
        }
    }

    private void updateTraces(ProjectVersion version, List<ArtifactAppEntity> artifacts, List<TraceAppEntity> traces) {

        Map<UUID, ArtifactAppEntity> artifactMap = new HashMap<>();
        for (ArtifactAppEntity artifact : artifacts) {
            artifactMap.put(artifact.getId(), artifact);
        }

        Map<Pair<String, String>, TraceMatrixEntry> seenTraceTypes = new HashMap<>();
        for (TraceAppEntity trace : traces) {
            ArtifactAppEntity source = artifactMap.get(trace.getSourceId());
            ArtifactAppEntity target = artifactMap.get(trace.getTargetId());

            Pair<String, String> typePair = new Pair<>(source.getType(), target.getType());
            if (!seenTraceTypes.containsKey(typePair)) {
                Optional<ArtifactType> sourceType =
                    typeRepository.findByProjectAndNameIgnoreCase(version.getProject(), source.getType());
                Optional<ArtifactType> targetType =
                    typeRepository.findByProjectAndNameIgnoreCase(version.getProject(), target.getType());

                TraceMatrixEntry entry = traceMatrixService
                    .getOrCreateEntry(version, sourceType.orElseThrow(), targetType.orElseThrow());
                entry.setCount(0);
                entry.setGeneratedCount(0);
                entry.setApprovedCount(0);

                seenTraceTypes.put(typePair, entry);
            }

            TraceMatrixEntry entry = seenTraceTypes.get(typePair);
            entry.setCount(entry.getCount() + 1);
            if (trace.getTraceType() == TraceType.GENERATED) {
                entry.setGeneratedCount(entry.getGeneratedCount() + 1);
                if (trace.getApprovalStatus() == ApprovalStatus.APPROVED) {
                    entry.setApprovedCount(entry.getApprovedCount() + 1);
                }
            }
        }

        for (TraceMatrixEntry entry : seenTraceTypes.values()) {
            traceMatrixService.updateEntry(entry);
        }
    }
}
