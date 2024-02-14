package edu.nd.crc.safa.features.generation.search;

import java.util.Set;
import java.util.UUID;
import javax.management.InvalidAttributeValueException;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.permissions.checks.billing.HasUnlimitedCreditsCheck;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import jakarta.validation.Valid;
import org.apache.commons.lang3.NotImplementedException;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SearchController extends BaseController {

    public SearchController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
    }

    /**
     * Performs search function for different modes of searching (e.g. prompt / artifacts / artifactTypes).
     *
     * @param versionId The ID of the project version to search in.
     * @param request   The request containing search criteria.
     * @return SearchResponse containing artifact ids and bodies.
     */
    @PostMapping(AppRoutes.Search.SEARCH)
    public SearchResponse search(@PathVariable UUID versionId, @RequestBody @Valid SearchRequest request)
        throws InvalidAttributeValueException {
        SafaUser user = getServiceProvider().getSafaUserService().getCurrentUser();
        ProjectVersion projectVersion =
            getResourceBuilder()
                .fetchVersion(versionId)
                .asUser(user)
                .withPermissions(Set.of(ProjectPermission.VIEW, ProjectPermission.GENERATE))
                .withAdditionalCheck(new HasUnlimitedCreditsCheck())
                .get();
        ProjectAppEntity projectAppEntity = getServiceProvider()
            .getProjectRetrievalService()
            .getProjectAppEntity(projectVersion);
        SearchResponse response = null;
        switch (request.getMode()) {
            case PROMPT:
                if (request.getPrompt() == null || request.getPrompt().equals("")) {
                    throw new InvalidAttributeValueException("Expected prompt to contain non-empty string.");
                }
                response = getServiceProvider().getSearchService().performPromptSearch(projectAppEntity,
                    request.getPrompt(), request.getSearchTypes(), request.getMaxResults());
                getServiceProvider().getSearchService().addRelatedTypes(projectAppEntity, response,
                    request.getRelatedTypes());
                return response;

            case ARTIFACTS:
                if (request.getArtifactIds() == null) {
                    throw new InvalidAttributeValueException("Expected artifactIds to be non-null.");
                }
                if (request.getArtifactIds().isEmpty()) {
                    return new SearchResponse();
                }
                response = getServiceProvider().getSearchService().performArtifactSearch(projectAppEntity,
                    request.getArtifactIds(), request.getSearchTypes(), request.getMaxResults());
                getServiceProvider().getSearchService().addRelatedTypes(projectAppEntity, response,
                    request.getRelatedTypes());
                return response;

            case ARTIFACTTYPES:
                if (request.getArtifactTypes() == null) {
                    throw new InvalidAttributeValueException("Expected artifactTypes to be non-null.");
                }
                if (request.getArtifactTypes().isEmpty()) {
                    return new SearchResponse();
                }
                throw new NotImplementedException("Generating between artifact types in under construction");
            default:
                throw new RuntimeException("Search mode is not implemented:" + request.getMode().name());
        }
    }
}
