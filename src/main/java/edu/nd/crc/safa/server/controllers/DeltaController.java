package edu.nd.crc.safa.server.controllers;

import java.util.UUID;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.api.ServerResponse;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.ProjectRepository;
import edu.nd.crc.safa.server.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.services.DeltaService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

/**
 * Provides endpoints for calculating the changes between two project versions.
 */
@RestController
public class DeltaController extends BaseController {

    DeltaService deltaService;

    @Autowired
    public DeltaController(ProjectRepository projectRepository,
                           ProjectVersionRepository projectVersionRepository,
                           ResourceBuilder resourceBuilder,
                           DeltaService deltaService) {
        super(projectRepository, projectVersionRepository, resourceBuilder);
        this.deltaService = deltaService;
    }

    /**
     * Returns ProjectDelta response object indicating changes in artifacts between the two versions specified.
     *
     * @param baselineVersionId UUID indicating the baseline version.
     * @param targetVersionId   UUID of the target version to compare the baseline against.
     * @return ProjectDelta with artifacts that were added, removed, and modified between versions.
     * @throws SafaError Throws error if baseline or target version is not found.
     */
    @GetMapping(AppRoutes.Projects.calculateProjectDelta)
    public ServerResponse calculateProjectDelta(@PathVariable UUID baselineVersionId,
                                                @PathVariable UUID targetVersionId) throws SafaError {
        ProjectVersion baselineVersion = this.resourceBuilder.fetchVersion(baselineVersionId).withViewVersion();
        ProjectVersion targetVersion = this.resourceBuilder.fetchVersion(targetVersionId).withViewVersion();
        return new ServerResponse(this.deltaService.calculateProjectDelta(baselineVersion, targetVersion));
    }
}
