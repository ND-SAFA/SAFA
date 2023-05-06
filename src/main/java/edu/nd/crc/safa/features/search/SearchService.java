package edu.nd.crc.safa.features.search;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.services.ProjectRetrievalService;
import edu.nd.crc.safa.features.tgen.entities.BaseGenerationModels;
import edu.nd.crc.safa.features.tgen.entities.api.TGenDataset;
import edu.nd.crc.safa.features.tgen.entities.api.TGenPredictionOutput;
import edu.nd.crc.safa.features.tgen.entities.api.TGenPredictionRequestDTO;
import edu.nd.crc.safa.features.tgen.method.TGen;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

/**
 * Provides searching functions to search endpoint.
 */
@AllArgsConstructor
@Service
public class SearchService {
    private static final String PROMPT_KEY = "PROMPT";
    private static final double THRESHOLD = 0.5;
    ProjectRetrievalService projectRetrievalService;

    /**
     * Searches for artifacts in search types that match the given prompt.
     *
     * @param projectVersion The project version of artifacts to use.
     * @param prompt         The prompt to match artifacts against.
     * @param searchTypes    The types of artifacts to match against.
     * @param tracingPrompt  The prompt used to determine if artifacts are related to prompt.
     * @return Ids of matched artifacts.
     */
    public SearchResponse performPromptSearch(ProjectVersion projectVersion, String prompt, List<String> searchTypes,
                                              String tracingPrompt) {
        ProjectAppEntity projectAppEntity = projectRetrievalService.getProjectAppEntity(projectVersion);
        Map<String, String> sourceLayer = new HashMap<>();
        sourceLayer.put(PROMPT_KEY, prompt);
        Map<UUID, String> targetLayer = constructTargetLayer(projectAppEntity, searchTypes);
        return searchSourceLayer(sourceLayer, convertArtifactMapToLayer(targetLayer), tracingPrompt);
    }

    /**
     * Searches for artifacts in search types using the artifacts as queries.
     *
     * @param projectVersion The project version of artifacts to search within.
     * @param artifactIds    The ids of the artifacts to use as queries.
     * @param searchTypes    The types of artifacts to match against.
     * @param tracingPrompt  The prompt used to determine if two artifacts are linked.
     * @return List of matched artifacts.
     */
    public SearchResponse performArtifactSearch(ProjectVersion projectVersion,
                                                List<UUID> artifactIds,
                                                List<String> searchTypes,
                                                String tracingPrompt) {
        ProjectAppEntity projectAppEntity = projectRetrievalService.getProjectAppEntity(projectVersion);
        Map<UUID, ArtifactAppEntity> artifactIdMap = projectAppEntity.getArtifactIdMap();
        Map<UUID, String> sourceLayer = createArtifactLayerFromIds(artifactIds, artifactIdMap);
        Map<UUID, String> targetLayer = constructTargetLayer(projectAppEntity, searchTypes);
        return searchSourceLayer(
            convertArtifactMapToLayer(sourceLayer),
            convertArtifactMapToLayer(targetLayer), tracingPrompt);
    }

    /**
     * Creates an artifact layer of artifacts whose Ids are specified.
     *
     * @param artifactIds   The ids of the artifacts to include in the layer.
     * @param artifactIdMap Map of id to artifacts to extract from.
     * @return Mapping between id and body of selected artifacts.
     */
    private Map<UUID, String> createArtifactLayerFromIds(List<UUID> artifactIds,
                                                         Map<UUID, ArtifactAppEntity> artifactIdMap) {
        Map<UUID, String> sourceLayer = new HashMap<>();
        for (UUID artifactId : artifactIds) {
            sourceLayer.put(artifactId, artifactIdMap.get(artifactId).getBody());
        }
        return sourceLayer;
    }

    /**
     * Creates artifact level extracted from artifacts types and project entities.
     *
     * @param projectAppEntity The project at a certain version containing artifacts and traces.
     * @param artifactTypes    The artifact types whose associated artifacts are being extracted.
     * @return The map between artifact id and body.
     */
    private Map<UUID, String> constructTargetLayer(ProjectAppEntity projectAppEntity, List<String> artifactTypes) {
        Map<UUID, String> targetLayer = new HashMap<>();
        for (String artifactTypeName : artifactTypes) {
            List<ArtifactAppEntity> artifacts = projectAppEntity.getByArtifactType(artifactTypeName);
            artifacts.forEach(a -> targetLayer.put(a.getId(), a.getBody()));
        }
        return targetLayer;
    }

    /**
     * Performs a search between source and target artifacts using TGEN tracing.
     *
     * @param sourceLayer   Source artifacts mapping id to body.
     * @param targetLayer   Target artifacts mapping id to body.
     * @param tracingPrompt The prompt used to determine if two artifacts should be traced.
     * @return Target Artifact IDs that matched source artifacts.
     */
    public SearchResponse searchSourceLayer(Map<String, String> sourceLayer, Map<String, String> targetLayer,
                                            String tracingPrompt) {

        TGenDataset dataset = new TGenDataset(List.of(sourceLayer), List.of(targetLayer));
        BaseGenerationModels model = BaseGenerationModels.GPT;
        TGenPredictionRequestDTO payload = new TGenPredictionRequestDTO(model.getStatePath(), dataset, tracingPrompt);
        System.out.println("PAYLOAD:" + payload);
        TGen controller = model.createTGenController();
        TGenPredictionOutput response = controller.performPrediction(payload);
        List<UUID> matchedArtifactIds = response.getPredictions().stream()
            .filter(t -> t.getScore() >= THRESHOLD)
            .map(TGenPredictionOutput.PredictedLink::getTarget)
            .filter(t -> !sourceLayer.containsKey(t))
            .map(UUID::fromString)
            .collect(Collectors.toList());
        List<String> matchedArtifactBodies =
            matchedArtifactIds.stream().map(UUID::toString).map(targetLayer::get).collect(Collectors.toList());
        return new SearchResponse(matchedArtifactIds, matchedArtifactBodies);
    }

    private Map<String, String> convertArtifactMapToLayer(Map<UUID, String> artifactMap) {
        return artifactMap.entrySet().stream()
            .collect(Collectors.toMap(entry -> entry.getKey().toString(), Map.Entry::getValue));
    }
}
