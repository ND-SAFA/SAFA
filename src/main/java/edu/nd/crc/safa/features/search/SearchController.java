package edu.nd.crc.safa.features.search;

import java.util.UUID;
import javax.management.InvalidAttributeValueException;
import javax.validation.Valid;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

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
     */
    @PostMapping(AppRoutes.Search.SEARCH)
    public SearchResponse search(@PathVariable UUID versionId, @RequestBody @Valid SearchRequest request) throws InvalidAttributeValueException {
        ProjectVersion projectVersion =
            this.resourceBuilder.fetchVersion(versionId).withEditVersion();
        switch (request.mode) {
            case PROMPT:
                if (request.prompt == null || request.prompt.equals("")) {
                    throw new InvalidAttributeValueException("Expected prompt to contain non-empty string.");
                }
                return this.serviceProvider.getSearchService().performPromptSearch(projectVersion,
                    request.getPrompt(), request.getSearchTypes(), request.getTracingPrompt());

            case ARTIFACTS:
                if (request.artifactIds == null) {
                    throw new InvalidAttributeValueException("Expected artifactIds to be non-null.");
                }
                if (request.artifactIds.isEmpty()) {
                    return new SearchResponse();
                }
                return this.serviceProvider.getSearchService().performArtifactSearch(projectVersion,
                    request.getArtifactIds(), request.getSearchTypes(), request.getTracingPrompt());
            case ARTIFACTTYPES:
                if (request.artifactTypes == null) {
                    throw new InvalidAttributeValueException("Expected artifactTypes to be non-null.");
                }
                if (request.artifactTypes.isEmpty()) {
                    return new SearchResponse();
                }
                throw new NotImplementedException("Generating between artifact types in under construction");
            default:
                throw new RuntimeException("Search mode is not implemented:" + request.mode.name());
        }
    }
}
