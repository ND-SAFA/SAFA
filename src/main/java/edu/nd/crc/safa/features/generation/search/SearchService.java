package edu.nd.crc.safa.features.generation.search;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.common.SafaRequestBuilder;
import edu.nd.crc.safa.features.generation.GenerationApi;
import edu.nd.crc.safa.features.generation.common.GenerationDataset;
import edu.nd.crc.safa.features.generation.common.GenerationLink;
import edu.nd.crc.safa.features.generation.common.TraceLayer;
import edu.nd.crc.safa.features.generation.tgen.TGenPredictionRequestDTO;
import edu.nd.crc.safa.features.generation.tgen.TGenTraceGenerationResponse;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.graph.ArtifactNode;
import edu.nd.crc.safa.features.projects.graph.ProjectGraph;
import edu.nd.crc.safa.features.projects.services.ProjectRetrievalService;
import edu.nd.crc.safa.utilities.ProjectDataStructures;

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
    SafaRequestBuilder safaRequestBuilder;

    /**
     * Searches for artifacts in search types that match the given prompt.
     *
     * @param projectAppEntity The project containing artifacts to search.
     * @param prompt           The prompt to match artifacts against.
     * @param searchTypes      The types of artifacts to match against.
     * @param n                The top n matches to return.
     * @return Ids of matched artifacts.
     */
    public SearchResponse performPromptSearch(ProjectAppEntity projectAppEntity, String prompt,
                                              List<String> searchTypes, int n) {
        Map<String, String> promptLayer = new HashMap<>();
        promptLayer.put(PROMPT_KEY, prompt);
        Map<UUID, String> artifactMap = constructTargetLayer(projectAppEntity, searchTypes);
        Map<String, String> artifactLayer = convertArtifactMapToLayer(artifactMap);
        return searchSourceLayer(promptLayer, artifactLayer, n);
    }

    /**
     * Searches for artifacts in search types using the artifacts as queries.
     *
     * @param projectAppEntity The project containing artifacts to search.
     * @param artifactIds      The ids of the artifacts to use as queries.
     * @param searchTypes      The types of artifacts to match against.
     * @param n                The number of entries to return.
     * @return List of matched artifacts.
     */
    public SearchResponse performArtifactSearch(ProjectAppEntity projectAppEntity,
                                                List<UUID> artifactIds,
                                                List<String> searchTypes, int n) {
        Map<UUID, ArtifactAppEntity> artifactIdMap = ProjectDataStructures.createArtifactMap(
            projectAppEntity.getArtifacts());
        Map<UUID, String> sourceLayer = createArtifactLayerFromIds(artifactIds, artifactIdMap);
        Map<UUID, String> targetLayer = constructTargetLayer(projectAppEntity, searchTypes);
        return searchSourceLayer(
            convertArtifactMapToLayer(sourceLayer),
            convertArtifactMapToLayer(targetLayer), n);
    }

    /**
     * Performs a search between source and target artifacts using TGEN tracing.
     *
     * @param promptLayer   Source artifacts mapping id to body.
     * @param artifactLayer Target artifacts mapping id to body.
     * @param n             The top n matches to return.
     * @return Target Artifact IDs that matched source artifacts.
     */
    public SearchResponse searchSourceLayer(Map<String, String> promptLayer,
                                            Map<String, String> artifactLayer, int n) {
        Map<String, Map<String, String>> artifactLayers = new HashMap<>();
        artifactLayers.put("prompt", promptLayer);
        artifactLayers.put("artifacts", artifactLayer);

        TraceLayer layer = new TraceLayer("artifacts", "prompt");
        GenerationDataset dataset = new GenerationDataset(artifactLayers, List.of(layer));
        TGenPredictionRequestDTO payload = new TGenPredictionRequestDTO(dataset);
        GenerationApi tgen = new GenerationApi(this.safaRequestBuilder);
        TGenTraceGenerationResponse response = tgen.performSearch(payload, null);
        List<UUID> matchedArtifactIds = response.getPredictions().stream()
            .filter(t -> t.getScore() >= THRESHOLD)
            .map(GenerationLink::getSource)
            .map(UUID::fromString)
            .collect(Collectors.toList());
        int maxIndex = Math.min(matchedArtifactIds.size(), n);
        matchedArtifactIds = matchedArtifactIds.subList(0, maxIndex);
        List<String> matchedArtifactBodies = matchedArtifactIds
            .stream().map(UUID::toString)
            .map(artifactLayer::get)
            .collect(Collectors.toList());
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
            artifacts
                .stream()
                .filter(a -> a.getTraceString().length() > 0)
                .forEach(a -> targetLayer.put(a.getId(), a.getTraceString()));
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
        ProjectGraph projectGraph = new ProjectGraph(projectAppEntity);
        Set<UUID> relatedArtifacts = new HashSet<>();
        for (UUID selectedArtifactId : selectedArtifactIds) {
            ArtifactNode artifactNode = projectGraph.getArtifactNode(selectedArtifactId);
            List<UUID> neighborIds = artifactNode.getNeighborhoodWithTypes(relatedTypes);
            relatedArtifacts.addAll(neighborIds);
        }
        return new ArrayList<>(relatedArtifacts);
    }

    private Map<String, String> convertArtifactMapToLayer(Map<UUID, String> artifactMap) {
        return artifactMap.entrySet().stream()
            .collect(Collectors.toMap(entry -> entry.getKey().toString(), Map.Entry::getValue));
    }
}


