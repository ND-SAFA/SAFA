package edu.nd.crc.safa.features.search;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import javax.management.InvalidAttributeValueException;
import javax.validation.Valid;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;

import org.apache.commons.lang3.NotImplementedException;
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
    public List<UUID> search(@RequestBody @Valid SearchRequest payload) throws InvalidAttributeValueException {
        switch (payload.mode) {
            case PROMPT:
                if (payload.prompt == null || payload.prompt.equals("")) {
                    throw new InvalidAttributeValueException("Expected prompt to contain non-empty string.");
                }
                return performPromptSearch(payload.prompt, payload.searchTypes);

            case ARTIFACTS:
                if (payload.artifactIds == null) {
                    throw new InvalidAttributeValueException("Expected artifactIds to be non-null.");
                }
                if (payload.artifactIds.isEmpty()) {
                    return new ArrayList<>();
                }
                return performArtifactSearch(payload.artifactIds, payload.searchTypes);
            case ARTIFACTTYPES:
                if (payload.artifactTypes == null) {
                    throw new InvalidAttributeValueException("Expected artifactTypes to be non-null.");
                }
                if (payload.artifactTypes.isEmpty()) {
                    return new ArrayList<>();
                }
                return performGeneration(payload.artifactTypes, payload.searchTypes);
            default:
                throw new RuntimeException("Search mode is not implemented:" + payload.mode.name());
        }
    }

    public List<UUID> performPromptSearch(String prompt, List<String> searchTypes) {
        throw new NotImplementedException("Tracing artifacts is under construction.");
    }

    public List<UUID> performArtifactSearch(List<UUID> artifactIds, List<String> searchTypes) {
        throw new NotImplementedException("Tracing artifacts is under construction.");
    }

    public List<UUID> performGeneration(List<String> sourceTypes, List<String> targetTypes) {
        throw new NotImplementedException("Generating between artifact types in under construction");
    }
}
