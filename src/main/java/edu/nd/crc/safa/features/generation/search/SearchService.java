package edu.nd.crc.safa.features.generation.search;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.generation.api.GenApi;
import edu.nd.crc.safa.features.generation.common.GenerationArtifact;
import edu.nd.crc.safa.features.generation.common.GenerationDataset;
import edu.nd.crc.safa.features.generation.common.GenerationLink;
import edu.nd.crc.safa.features.generation.common.TraceLayer;
import edu.nd.crc.safa.features.generation.tgen.TGenRequest;
import edu.nd.crc.safa.features.generation.tgen.TGenResponse;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.graph.ArtifactNode;
import edu.nd.crc.safa.features.projects.graph.ProjectGraph;
import edu.nd.crc.safa.utilities.ProjectDataStructures;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

/**
 * Provides searching functions to search endpoint.
 */
@AllArgsConstructor
@Service
public class SearchService {
    private static final String PROMPT_TYPE = "PROMPT_TYPE";
    private static final String PROMPT_KEY = "PROMPT";
    private static final String ARTIFACT_KEY = "artifacts";
    private static final double THRESHOLD = 0.5;
    private final GenApi genApi;

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
        ArtifactAppEntity promptArtifact = new ArtifactAppEntity();
        promptArtifact.setName(PROMPT_KEY);
        promptArtifact.setBody(prompt);
        promptArtifact.setType(PROMPT_KEY);
        List<ArtifactAppEntity> artifacts = constructTargetLayer(projectAppEntity, searchTypes);
        artifacts.add(promptArtifact);
        return searchSourceLayer(artifacts, searchTypes, n);
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
        List<ArtifactAppEntity> queries = artifactIds.stream().map(artifactIdMap::get)
            .collect(Collectors.toList());
        queries.forEach(a -> a.setType(PROMPT_KEY));
        List<ArtifactAppEntity> candidateArtifacts = constructTargetLayer(projectAppEntity, searchTypes);
        List<ArtifactAppEntity> artifacts = new ArrayList<>();
        artifacts.addAll(queries);
        artifacts.addAll(candidateArtifacts);
        return searchSourceLayer(artifacts, searchTypes, n);
    }

    /**
     * Performs a search between source and target artifacts using TGEN tracing.
     *
     * @param artifacts   The artifacts containing queries and candidate artifacts.
     * @param n           The top n matches to return.
     * @param searchTypes The artifact types to search against.
     * @return Target Artifact IDs that matched source artifacts.
     */
    public SearchResponse searchSourceLayer(List<ArtifactAppEntity> artifacts, List<String> searchTypes, int n) {
        List<TraceLayer> traceLayers = new ArrayList<>();
        for (String searchType : searchTypes) {
            traceLayers.add(new TraceLayer(searchType, PROMPT_KEY));
        }
        Map<String, ArtifactAppEntity> artifactMap = ProjectDataStructures.createArtifactNameMap(artifacts);
        List<GenerationArtifact> generationArtifacts = artifacts.stream()
            .map(GenerationArtifact::new).collect(Collectors.toList());
        GenerationDataset dataset = new GenerationDataset(generationArtifacts, traceLayers);
        TGenRequest payload = new TGenRequest(dataset);
        TGenResponse response = this.genApi.performSearch(payload, null);
        List<UUID> matchedArtifactIds = response.getPredictions().stream()
            .filter(t -> t.getScore() >= THRESHOLD)
            .map(GenerationLink::getSource)
            .map(artifactMap::get)
            .map(ArtifactAppEntity::getId)
            .collect(Collectors.toList());
        int maxIndex = Math.min(matchedArtifactIds.size(), n);
        matchedArtifactIds = matchedArtifactIds.subList(0, maxIndex);
        return new SearchResponse(matchedArtifactIds);
    }

    /**
     * Extracts the artifacts of associated type and converts them to
     *
     * @param projectAppEntity The project at a certain version containing artifacts and traces.
     * @param artifactTypes    The artifact types whose associated artifacts are being extracted.
     * @return The map between artifact id and body.
     */
    private List<ArtifactAppEntity> constructTargetLayer(ProjectAppEntity projectAppEntity,
                                                         List<String> artifactTypes) {
        List<ArtifactAppEntity> artifacts = new ArrayList<>();
        for (String artifactTypeName : artifactTypes) {
            artifacts.addAll(projectAppEntity.getByArtifactType(artifactTypeName));
        }
        return artifacts;
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
}


