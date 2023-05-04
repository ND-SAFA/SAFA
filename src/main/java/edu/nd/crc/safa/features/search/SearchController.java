package edu.nd.crc.safa.features.search;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.stream.Collectors;
import javax.management.InvalidAttributeValueException;
import javax.validation.Valid;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.tgen.entities.BaseGenerationModels;
import edu.nd.crc.safa.features.tgen.entities.api.TGenDataset;
import edu.nd.crc.safa.features.tgen.entities.api.TGenPredictionOutput;
import edu.nd.crc.safa.features.tgen.entities.api.TGenPredictionRequestDTO;
import edu.nd.crc.safa.features.tgen.method.TGen;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import org.apache.commons.lang3.NotImplementedException;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SearchController extends BaseController {
    private final static String PROMPT_KEY = "PROMPT";
    private final static double THRESHOLD = 0.5;

    public SearchController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
    }

    /**
     * Performs search function for different modes of searching (e.g. prompt / artifacts / artifactTypes).
     */
    @PostMapping(AppRoutes.Search.SEARCH)
    public List<UUID> search(@PathVariable UUID versionId, @RequestBody @Valid SearchRequest request) throws InvalidAttributeValueException {
        ProjectVersion projectVersion =
            this.resourceBuilder.fetchVersion(versionId).withEditVersion();
        switch (request.mode) {
            case PROMPT:
                if (request.prompt == null || request.prompt.equals("")) {
                    throw new InvalidAttributeValueException("Expected prompt to contain non-empty string.");
                }
                return performPromptSearch(projectVersion, request);

            case ARTIFACTS:
                if (request.artifactIds == null) {
                    throw new InvalidAttributeValueException("Expected artifactIds to be non-null.");
                }
                if (request.artifactIds.isEmpty()) {
                    return new ArrayList<>();
                }
                return performArtifactSearch(projectVersion, request);
            case ARTIFACTTYPES:
                if (request.artifactTypes == null) {
                    throw new InvalidAttributeValueException("Expected artifactTypes to be non-null.");
                }
                if (request.artifactTypes.isEmpty()) {
                    return new ArrayList<>();
                }
                return performGeneration(request.artifactTypes, request.searchTypes);
            default:
                throw new RuntimeException("Search mode is not implemented:" + request.mode.name());
        }
    }

    public List<UUID> performPromptSearch(ProjectVersion projectVersion, SearchRequest request) {
        SafaUser user = this.serviceProvider.getSafaUserService().getCurrentUser();
        ProjectAppEntity projectAppEntity = this.serviceProvider
            .getProjectRetrievalService()
            .getProjectAppEntity(user, projectVersion);

        Map<String, String> sourceLayer = new HashMap<>() {{
            put(PROMPT_KEY, request.getPrompt());
        }};
        return searchSourceLayer(request, projectAppEntity, sourceLayer);
    }


    public List<UUID> performArtifactSearch(ProjectVersion projectVersion,
                                            SearchRequest request) throws InvalidAttributeValueException {
        SafaUser user = this.serviceProvider.getSafaUserService().getCurrentUser();
        ProjectAppEntity projectAppEntity = this.serviceProvider
            .getProjectRetrievalService()
            .getProjectAppEntity(user, projectVersion);
        Map<String, ArtifactAppEntity> artifactIdMap = projectAppEntity.getArtifactIdMap();
        Map<String, String> sourceLayer = new HashMap<>();
        for (UUID artifactUUID : request.getArtifactIds()) {
            String artifactId = artifactUUID.toString();
            if (!artifactIdMap.containsKey(artifactId)) {
                throw new InvalidAttributeValueException("Could not find artifact with id:" + artifactId);
            }
            sourceLayer.put(artifactId, artifactIdMap.get(artifactId).getBody());
        }

        return searchSourceLayer(request, projectAppEntity, sourceLayer);
    }

    private List<UUID> searchSourceLayer(SearchRequest request, ProjectAppEntity projectAppEntity, Map<String, String> sourceLayer) {
        Map<String, String> targetLayer = new HashMap<>();
        for (String artifactTypeName : request.getSearchTypes()) {
            List<ArtifactAppEntity> artifacts = projectAppEntity.getByArtifactType(artifactTypeName);
            artifacts.forEach(a -> targetLayer.put(a.getId().toString(), a.getBody()));
        }

        TGenDataset dataset = new TGenDataset(List.of(sourceLayer), List.of(targetLayer));
        BaseGenerationModels model = BaseGenerationModels.GPT;
        TGenPredictionRequestDTO payload = new TGenPredictionRequestDTO(model.getStatePath(), dataset);

        TGen controller = model.createTGenController();
        TGenPredictionOutput response = controller.performPrediction(payload);
        List<UUID> artifactTraced =
            response.getPredictions().stream()
                .map(t -> t.getTarget())
                .filter(t -> !sourceLayer.containsKey(t))
                .map(aId -> UUID.fromString(aId))
                .collect(Collectors.toList());
        return artifactTraced;
    }

    public List<UUID> performGeneration(List<String> sourceTypes, List<String> targetTypes) {
        throw new NotImplementedException("Generating between artifact types in under construction");
    }
}
