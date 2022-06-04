package edu.nd.crc.safa.server.controllers;

import java.util.List;
import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.services.retrieval.AppEntityRetrievalService;
import edu.nd.crc.safa.warnings.RuleName;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

/**
 * Responsible for creating, retrieving, and deleting warnings
 * in projects.
 */
@RestController
public class WarningController extends BaseController {

    private final AppEntityRetrievalService appEntityRetrievalService;

    @Autowired
    public WarningController(ResourceBuilder resourceBuilder,
                             AppEntityRetrievalService appEntityRetrievalService) {
        super(resourceBuilder);
        this.appEntityRetrievalService = appEntityRetrievalService;
    }

    /**
     * Returns the current warnings in the artifact tree of given project version.
     *
     * @param versionId The ID of the project version whose warnings are retrieved.
     * @return Mapping of artifact id's to the warnings objects present in those artifacts.
     * @throws SafaError Throws error if user does not have read permission on project version.
     */
    @GetMapping(AppRoutes.Projects.Warnings.getWarningsInProjectVersion)
    public Map<String, List<RuleName>> getWarningsInProjectVersion(@PathVariable UUID versionId) throws SafaError {
        ProjectVersion projectVersion = this.resourceBuilder.fetchVersion(versionId).withViewVersion();
        return this.appEntityRetrievalService.retrieveWarningsInProjectVersion(projectVersion);
    }
}
