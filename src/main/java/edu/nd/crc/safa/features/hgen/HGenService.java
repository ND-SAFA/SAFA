package edu.nd.crc.safa.features.hgen;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.services.ArtifactService;
import edu.nd.crc.safa.features.summary.TGenSummaryArtifact;
import edu.nd.crc.safa.features.summary.TGenSummaryArtifactType;
import edu.nd.crc.safa.features.tgen.entities.BaseGenerationModels;
import edu.nd.crc.safa.features.tgen.method.TGen;
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
    public List<String> generateHierarchy(ProjectVersion projectVersion, HGenRequestDTO request) {
        BaseGenerationModels baseModel = request.getModel();
        TGen controller = baseModel.createTGenController();
        Map<String, TGenSummaryArtifact> artifacts = createArtifacts(projectVersion, request.getArtifacts());
        List<List<String>> clusters = List.of(new ArrayList<>(artifacts.keySet()));
        TGenHGenRequest tgenRequest = new TGenHGenRequest(artifacts, clusters, baseModel.name());
        TGenHGenResponse response = controller.generateHierarchy(tgenRequest);
        return response.getArtifacts();
    }

    private Map<String, TGenSummaryArtifact> createArtifacts(ProjectVersion projectVersion, List<UUID> artifactIds) {
        List<ArtifactAppEntity> artifacts = artifactService.getAppEntities(projectVersion);
        Map<String, TGenSummaryArtifact> artifactMap = new HashMap<>();
        Set<UUID> artifactIdSet = new HashSet<>(artifactIds);
        artifacts.stream()
            .filter(a -> artifactIdSet.contains(a.getId()))
            .forEach(a -> {
                TGenSummaryArtifactType chunkerType = TGenSummaryArtifactType.getArtifactType(a.getName());
                artifactMap.put(a.getId().toString(), new TGenSummaryArtifact(a.getName(), a.getName(), a.getBody(),
                    chunkerType));
            });
        return artifactMap;
    }
}
