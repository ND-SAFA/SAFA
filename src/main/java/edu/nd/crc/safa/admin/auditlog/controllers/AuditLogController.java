package edu.nd.crc.safa.admin.auditlog.controllers;

import java.time.LocalDateTime;
import java.util.List;

import edu.nd.crc.safa.admin.auditlog.entities.app.AuditLogEntryDTO;
import edu.nd.crc.safa.admin.auditlog.services.AuditLogService;
import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.permissions.services.PermissionService;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class AuditLogController extends BaseController {

    private final AuditLogService auditLogService;
    private final PermissionService permissionService;

    public AuditLogController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider,
                              AuditLogService auditLogService, PermissionService permissionService) {
        super(resourceBuilder, serviceProvider);
        this.auditLogService = auditLogService;
        this.permissionService = permissionService;
    }

    @GetMapping(AppRoutes.Audit.LOGS)
    public List<AuditLogEntryDTO> getLogs(@RequestParam(required = false) LocalDateTime before,
                                          @RequestParam(required = false) LocalDateTime after) {
        permissionService.requireSuperuser(getCurrentUser());

        if (before == null) {
            before = LocalDateTime.now();
        }
        if (after == null) {
            after = LocalDateTime.MIN;
        }

        return auditLogService.getBetween(before, after)
                .stream()
                .map(AuditLogEntryDTO::new)
                .toList();
    }
}
