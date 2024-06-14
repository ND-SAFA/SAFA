package edu.nd.crc.safa.admin.usagestats.controllers;

import java.util.UUID;

import edu.nd.crc.safa.admin.usagestats.entities.app.OnboardingProgressSummaryDTO;
import edu.nd.crc.safa.admin.usagestats.entities.app.UserStatisticsDTO;
import edu.nd.crc.safa.admin.usagestats.services.ApplicationUsageStatisticsService;
import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.permissions.services.PermissionService;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.services.SafaUserService;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class UsageStatisticsController extends BaseController {
    private final ApplicationUsageStatisticsService appUsageStatsService;
    private final PermissionService permissionService;
    private final SafaUserService userService;

    public UsageStatisticsController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider,
                                     ApplicationUsageStatisticsService appUsageStatsService,
                                     PermissionService permissionService, SafaUserService userService) {
        super(resourceBuilder, serviceProvider);
        this.appUsageStatsService = appUsageStatsService;
        this.permissionService = permissionService;
        this.userService = userService;
    }

    @GetMapping(AppRoutes.Statistics.ONBOARDING_ROOT)
    public OnboardingProgressSummaryDTO getOrientationProgressSummary() {
        permissionService.requireSuperuser(getCurrentUser());
        return appUsageStatsService.getOrientationProgressSummary();
    }

    @GetMapping(AppRoutes.Statistics.ONBOARDING_BY_USER)
    public UserStatisticsDTO getOrientationProgressForUser(@PathVariable UUID userId) {
        permissionService.requireSuperuser(getCurrentUser());
        SafaUser user = userService.getUserById(userId);
        return new UserStatisticsDTO(appUsageStatsService.getByUser(user));
    }
}
