package edu.nd.crc.safa.features.delta.controllers;

import java.util.UUID;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.delta.entities.app.ProjectDelta;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

/**
 * Provides endpoints for calculating the changes between two project versions.
 */
@RestController
public class DeltaController extends BaseController {

    @Autowired
    public DeltaController(ResourceBuilder resourceBuilder,
                           ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
    }

    /**
     * Returns ProjectDelta response object indicating changes in artifacts between the two versions specified.
     *
     * @param baselineVersionId UUID indicating the baseline version.
     * @param targetVersionId   UUID of the target version to compare the baseline against.
     * @return ProjectDelta with artifacts that were added, removed, and modified between versions.
     * @throws SafaError Throws error if baseline or target version is not found.
     */
    @GetMapping(AppRoutes.Delta.CALCULATE_PROJECT_DELTA)
    public ProjectDelta calculateProjectDelta(@PathVariable UUID baselineVersionId,
                                              @PathVariable UUID targetVersionId) throws SafaError {
        SafaUser user = getServiceProvider().getSafaUserService().getCurrentUser();
        ProjectVersion baselineVersion = getResourceBuilder().fetchVersion(baselineVersionId)
                .withPermission(ProjectPermission.VIEW, user).get();
        ProjectVersion targetVersion = getResourceBuilder().fetchVersion(targetVersionId)
                .withPermission(ProjectPermission.VIEW, user).get();
        return getServiceProvider().getDeltaService().calculateProjectDelta(baselineVersion, targetVersion);
    }
}
