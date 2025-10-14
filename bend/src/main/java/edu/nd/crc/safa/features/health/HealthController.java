package edu.nd.crc.safa.features.health;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.health.entities.HealthRequest;
import edu.nd.crc.safa.features.health.entities.HealthResponseDTO;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HealthController extends BaseController {
    public HealthController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
    }

    @PostMapping(AppRoutes.Health.HEALTH)
    public HealthResponseDTO generateHealthTasks(@Valid @RequestBody HealthRequest request) {
        SafaUser currentUser = getCurrentUser();
        ProjectVersion projectVersion = getResourceBuilder()
            .fetchVersion(request.getVersionId())
            .asUser(currentUser)
            .withPermission(ProjectPermission.EDIT)
            .get();
        return getServiceProvider().getHealthService().performHealthChecks(
            currentUser,
            projectVersion,
            request
        );
    }
}
