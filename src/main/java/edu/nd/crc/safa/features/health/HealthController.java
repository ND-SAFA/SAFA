package edu.nd.crc.safa.features.health;

import java.util.UUID;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.health.entities.HealthResponseDTO;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HealthController extends BaseController {
    public HealthController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
    }

    /**
     * Generates health checks for an artifact.
     *
     * @param versionId ID of version artifact.
     * @param artifact  Artifact generating health checks for.
     * @return Response containing all health checks found.
     */
    @PostMapping(AppRoutes.Health.GENERATE)
    public HealthResponseDTO generateHealthChecks(@PathVariable UUID versionId,
                                                  @RequestBody ArtifactAppEntity artifact) {
        SafaUser currentUser = getCurrentUser();
        ProjectVersion projectVersion = getResourceBuilder()
            .fetchVersion(versionId)
            .asUser(currentUser)
            .withPermission(ProjectPermission.EDIT)
            .get();
        return getServiceProvider().getHealthService().performArtifactHealthChecks(projectVersion, artifact);
    }
}
