package edu.nd.crc.safa.features.users.services;

import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.permissions.services.PermissionService;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

/**
 * Provides api for adding members and verifying status within project.
 */
@Service
@AllArgsConstructor
public class PermissionCheckerService {

    // TODO merge into other permission system

    private final PermissionService permissionService;

    public boolean hasViewPermission(JobDbEntity job, SafaUser user) {
        return permissionService.isSuperuser(user)
                || job.getUser().getUserId().equals(user.getUserId());
    }
}
