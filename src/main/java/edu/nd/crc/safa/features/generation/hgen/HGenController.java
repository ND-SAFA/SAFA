package edu.nd.crc.safa.features.generation.hgen;

import java.util.UUID;
import javax.validation.Valid;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.builders.HGenJobBuilder;
import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

/**
 * Provides endpoints for creating parent artifacts.
 */
@RestController
public class HGenController extends BaseController {
    public HGenController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
    }

    /**
     * Generates hierarchy above artifacts in request.
     *
     * @param versionId The Id of the version to collect artifacts in.
     * @param request   Contains artifacts and clusters within them.
     * @return List of generates artifacts for new level.
     */
    @PostMapping(AppRoutes.HGen.GENERATE)
    public JobAppEntity generateHierarchy(@PathVariable UUID versionId,
                                          @RequestBody @Valid HGenRequest request) throws Exception {
        SafaUser currentUser = this.serviceProvider.getSafaUserService().getCurrentUser();
        ProjectVersion projectVersion = this.resourceBuilder.fetchVersion(versionId)
                .withPermission(ProjectPermission.VIEW, currentUser).get();
        HGenJobBuilder jobBuilder = new HGenJobBuilder(this.serviceProvider, projectVersion, request, currentUser);
        return jobBuilder.perform();
    }
}
