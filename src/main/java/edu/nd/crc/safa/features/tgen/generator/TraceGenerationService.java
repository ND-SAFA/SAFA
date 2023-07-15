package edu.nd.crc.safa.features.tgen.generator;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.models.ITraceGenerationController;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.tgen.api.TGenDataset;
import edu.nd.crc.safa.features.tgen.entities.ArtifactLevelRequest;
import edu.nd.crc.safa.features.tgen.entities.TraceGenerationRequest;
import edu.nd.crc.safa.features.tgen.entities.TracingRequest;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.ApprovalStatus;
import edu.nd.crc.safa.utilities.ProjectDataStructures;

import lombok.AllArgsConstructor;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Service;

/**
 * Responsible for generating trace links for given projects.
 */
@Service
@AllArgsConstructor
@Scope("singleton")
public class TraceGenerationService {
    private static final String DELIMITER = "*";
    ITraceGenerationController traceGenerationController;

    /**
     * Retrieves artifacts associated with the source and target types defined in the tracing request.
     *
     * @param tracingRequest   The request detailing the artifacts to trace and the model to do so with.
     * @param projectAppEntity The project app entity containing artifacts and links.
     * @return TracingPayload detailing the artifacts and the method to trace with.
     */
    public static TGenDataset extractPayload(TracingRequest tracingRequest,
                                             ProjectAppEntity projectAppEntity) {
        Map<String, Map<String, String>> artifactLayers = new HashMap<>();
        List<List<String>> layers = new ArrayList<>();
        for (ArtifactLevelRequest artifactLevelRequest : tracingRequest.getArtifactLevels()) {
            String childType = artifactLevelRequest.getSource();
            String parentType = artifactLevelRequest.getTarget();

            for (String artifactType : List.of(childType, parentType)) {
                artifactLayers.computeIfAbsent(artifactType, t -> {
                    List<ArtifactAppEntity> artifacts = projectAppEntity.getByArtifactType(t);
                    return ProjectDataStructures.createArtifactLayer(artifacts);
                });
            }
            layers.add(List.of(childType, parentType));
        }
        return new TGenDataset(artifactLayers, layers);
    }

    public List<TraceAppEntity> generateTraceLinks(TraceGenerationRequest traceGenerationRequest,
                                                   ProjectAppEntity projectAppEntity) {
        List<TraceAppEntity> generatedTraces = new ArrayList<>();
        for (TracingRequest tracingRequest : traceGenerationRequest.getRequests()) {
            TGenDataset tracingPayload = extractPayload(tracingRequest, projectAppEntity);
            generatedTraces.addAll(generateLinksWithMethod(tracingPayload));
        }
        return generatedTraces;
    }

    public List<TraceAppEntity> generateLinksWithMethod(TGenDataset tracingPayload) {
        return new ArrayList<>(traceGenerationController.generateLinks(tracingPayload, null));
    }

    public List<TraceAppEntity> filterDuplicateGeneratedLinks(List<TraceAppEntity> manualLinks,
                                                              List<TraceAppEntity> generatedLinks) {
        List<String> approvedLinks = manualLinks.stream()
            .filter(link -> link.getApprovalStatus() == ApprovalStatus.APPROVED)
            .map(link -> link.getSourceName() + DELIMITER + link.getTargetName())
            .collect(Collectors.toList());

        return generatedLinks
            .stream()
            .filter(t -> {
                String tId = t.getSourceName() + DELIMITER + t.getTargetName();
                return !approvedLinks.contains(tId);
            })
            .collect(Collectors.toList());
    }
}
