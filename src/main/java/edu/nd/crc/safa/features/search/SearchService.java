package edu.nd.crc.safa.features.search;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.services.ProjectRetrievalService;
import edu.nd.crc.safa.features.tgen.api.TGenDataset;
import edu.nd.crc.safa.features.tgen.api.TGenPredictionOutput;
import edu.nd.crc.safa.features.tgen.api.TGenPredictionRequestDTO;
import edu.nd.crc.safa.features.tgen.entities.BaseGenerationModels;
import edu.nd.crc.safa.features.tgen.method.TGen;

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
     * @param projectAppEntity The project containing artifacts to search.
     * @param prompt           The prompt to match artifacts against.
     * @param searchTypes      The types of artifacts to match against.
     * @param tracingPrompt    The prompt used to determine if artifacts are related to prompt.
     * @param model            The base model to use for searching.
     * @return Ids of matched artifacts.
     */
    public SearchResponse performPromptSearch(ProjectAppEntity projectAppEntity, String prompt,
                                              List<String> searchTypes, String tracingPrompt,
                                              BaseGenerationModels model) {
        Map<String, String> sourceLayer = new HashMap<>();
        sourceLayer.put(PROMPT_KEY, prompt);
        Map<UUID, String> targetLayer = constructTargetLayer(projectAppEntity, searchTypes);
        return searchSourceLayer(sourceLayer, convertArtifactMapToLayer(targetLayer), tracingPrompt, model);
    }

    /**
     * Searches for artifacts in search types using the artifacts as queries.
     *
     * @param projectAppEntity The project containing artifacts to search.
     * @param artifactIds      The ids of the artifacts to use as queries.
     * @param searchTypes      The types of artifacts to match against.
     * @param tracingPrompt    The prompt used to determine if two artifacts are linked.
     * @param model            The base model to use for searching.
     * @return List of matched artifacts.
     */
    public SearchResponse performArtifactSearch(ProjectAppEntity projectAppEntity,
                                                List<UUID> artifactIds,
                                                List<String> searchTypes,
                                                String tracingPrompt,
                                                BaseGenerationModels model) {
        Map<UUID, ArtifactAppEntity> artifactIdMap = projectAppEntity.getArtifactIdMap();
        Map<UUID, String> sourceLayer = createArtifactLayerFromIds(artifactIds, artifactIdMap);
        Map<UUID, String> targetLayer = constructTargetLayer(projectAppEntity, searchTypes);
        return searchSourceLayer(
            convertArtifactMapToLayer(sourceLayer),
            convertArtifactMapToLayer(targetLayer), tracingPrompt, model);
    }

    /**
     * Performs a search between source and target artifacts using TGEN tracing.
     *
     * @param sourceLayer   Source artifacts mapping id to body.
     * @param targetLayer   Target artifacts mapping id to body.
     * @param tracingPrompt The prompt used to determine if two artifacts should be traced.
     * @param model         The model to use for searching.
     * @return Target Artifact IDs that matched source artifacts.
     */
    public SearchResponse searchSourceLayer(Map<String, String> sourceLayer,
                                            Map<String, String> targetLayer,
                                            String tracingPrompt,
                                            BaseGenerationModels model) {

        TGenDataset dataset = new TGenDataset(List.of(sourceLayer), List.of(targetLayer));
        TGenPredictionRequestDTO payload = new TGenPredictionRequestDTO(model.getStatePath(), dataset, tracingPrompt);
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
            artifacts.forEach(a -> targetLayer.put(a.getId(), a.getTraceString()));
        }
        return targetLayer;
    }

    /**
     * Adds related types to search response.
     *
     * @param projectAppEntity The project to extract links between artifacts from.
     * @param response         The response of the search query.
     * @param relatedTypes     The related artifacts.
     * @return SearchResponse with added related types.
     */
    public SearchResponse addRelatedTypes(ProjectAppEntity projectAppEntity, SearchResponse response,
                                          List<String> relatedTypes) {
        Set<UUID> selectedArtifactSet = new HashSet<>(response.getArtifactIds());
        Set<String> relatedTypesSet = new HashSet<>(relatedTypes);
        List<UUID> relatedArtifacts = calculateRelatedTypes(projectAppEntity, selectedArtifactSet, relatedTypesSet);
        response.getArtifactIds().addAll(relatedArtifacts);
        //TODO : Missing related types body, but removing in future
        return response;
    }

    private List<UUID> calculateRelatedTypes(ProjectAppEntity projectAppEntity, Set<UUID> selectedArtifactIds,
                                             Set<String> relatedTypes) {
        Map<UUID, ArtifactAppEntity> artifactMap = projectAppEntity.getArtifactIdMap();
        List<UUID> relatedArtifacts = new ArrayList<>();
        projectAppEntity
            .getTraces()
            .forEach(t -> {
                if (selectedArtifactIds.contains(t.getSourceId())) {
                    ArtifactAppEntity targetArtifact = artifactMap.get(t.getTargetId());
                    if (relatedTypes.contains(targetArtifact.getType())) {
                        relatedArtifacts.add(targetArtifact.getId());
                    }
                }
                if (selectedArtifactIds.contains(t.getTargetId())) {
                    ArtifactAppEntity sourceArtifact = artifactMap.get(t.getSourceId());
                    if (relatedTypes.contains(sourceArtifact.getType())) {
                        relatedArtifacts.add(sourceArtifact.getId());
                    }
                }
            });
        return relatedArtifacts;
    }

    private Map<String, String> convertArtifactMapToLayer(Map<UUID, String> artifactMap) {
        return artifactMap.entrySet().stream()
            .collect(Collectors.toMap(entry -> entry.getKey().toString(), Map.Entry::getValue));
    }
}


