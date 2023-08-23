package edu.nd.crc.safa.features.users.services;

import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
 * Provides api for adding members and verifying status within project.
 */
@Service
public class PermissionCheckerService {

    @Autowired
    public PermissionCheckerService() {
    }

    public boolean hasViewPermission(JobDbEntity job, SafaUser user) {
        return job.getUser().getUserId().equals(user.getUserId());
    }
}
