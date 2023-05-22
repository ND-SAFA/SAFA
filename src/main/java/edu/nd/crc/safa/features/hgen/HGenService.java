package edu.nd.crc.safa.features.hgen;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.services.ArtifactService;
import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.summary.TGenSummaryArtifact;
import edu.nd.crc.safa.features.summary.TGenSummaryArtifactType;
import edu.nd.crc.safa.features.tgen.entities.BaseGenerationModels;
import edu.nd.crc.safa.features.tgen.method.TGen;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

/**
 * Provides API for generating hierarchy of artifacts.
 */
@AllArgsConstructor
@Service
public class HGenService {
    ArtifactService artifactService;

    /**
     * Generates artifacts for each cluster defined.
     *
     * @param projectVersion The version to retrieve artifacts in.
     * @param request        The request defining artifacts, clusters, and model.
     * @return List of generated artifacts.
     */
    public ProjectCommit generateHierarchy(ProjectVersion projectVersion, HGenRequestDTO request) {
        BaseGenerationModels baseModel = request.getModel();
        String targetType = request.getTargetType();
        TGen controller = baseModel.createTGenController();
        List<TGenSummaryArtifact> artifacts = createArtifacts(projectVersion, request.getArtifacts());
        TGenHGenRequest tgenRequest = new TGenHGenRequest(artifacts, targetType, request.getClusters(),
            baseModel.name());
        TGenHGenResponse response = controller.generateHierarchy(tgenRequest);
        List<ArtifactAppEntity> artifactsGenerated = response.getDataset().getTargetLayers().get(0).entrySet().stream()
            .map(entry -> {
                ArtifactAppEntity artifact = new ArtifactAppEntity();
                artifact.setBody(entry.getValue());
                artifact.setName(entry.getKey());
                return artifact;
            }).collect(Collectors.toList());
        List<TraceAppEntity> generatedTraces = response.getDataset().getTrueLinks().stream().map(t -> {
            String sourceName = t.get(0);
            String targetName = t.get(1);
            TraceAppEntity traceAppEntity = new TraceAppEntity();
            traceAppEntity.setSourceName(sourceName);
            traceAppEntity.setTargetName(targetName);
            return traceAppEntity;
        }).collect(Collectors.toList());
        ProjectCommit projectCommit = new ProjectCommit();
        projectCommit.addArtifacts(ModificationType.ADDED, artifactsGenerated);
        projectCommit.addTraces(ModificationType.ADDED, generatedTraces);
        return projectCommit;
    }

    private List<TGenSummaryArtifact> createArtifacts(ProjectVersion projectVersion, List<UUID> artifactIds) {
        List<ArtifactAppEntity> artifacts = artifactService.getAppEntities(projectVersion);
        List<TGenSummaryArtifact> preparedArtifacts = new ArrayList<>();
        Set<UUID> artifactIdSet = new HashSet<>(artifactIds);
        artifacts.stream()
            .filter(a -> artifactIdSet.contains(a.getId()))
            .forEach(a -> {
                TGenSummaryArtifactType chunkerType = TGenSummaryArtifactType.getArtifactType(a.getName());
                preparedArtifacts.add(new TGenSummaryArtifact(
                    a.getId().toString(), a.getName(), a.getBody(), chunkerType));
            });
        return preparedArtifacts;
    }
}
