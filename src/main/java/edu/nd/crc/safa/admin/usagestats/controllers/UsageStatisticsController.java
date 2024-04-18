package edu.nd.crc.safa.admin.usagestats.controllers;

import edu.nd.crc.safa.admin.usagestats.entities.app.UserProgressSummaryAppEntity;
import edu.nd.crc.safa.admin.usagestats.services.ApplicationUsageStatisticsService;
import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.permissions.services.PermissionService;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class UsageStatisticsController extends BaseController {
    private final ApplicationUsageStatisticsService appUsageStatsService;
    private final PermissionService permissionService;

    public UsageStatisticsController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider,
                                     ApplicationUsageStatisticsService appUsageStatsService,
                                     PermissionService permissionService) {
        super(resourceBuilder, serviceProvider);
        this.appUsageStatsService = appUsageStatsService;
        this.permissionService = permissionService;
    }

    @GetMapping(AppRoutes.Statistics.ONBOARDING_ALL_USERS)
    public UserProgressSummaryAppEntity getOrientationProgressSummary() {
        permissionService.requireSuperuser(getCurrentUser());
        return appUsageStatsService.getOrientationProgressSummary();
    }
}
