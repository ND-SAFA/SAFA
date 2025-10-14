package edu.nd.crc.safa.features.notifications.security;

import java.util.UUID;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.notifications.members.DestinationPath;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

/**
 * Topic permission check for jobs
 */
public class JobTopicPermissionCheck implements TopicPermissionCheckFunction {
    @Override
    public boolean canSubscribe(SafaUser user, DestinationPath destinationPath) {
        ServiceProvider serviceProvider = ServiceProvider.getInstance();
        UUID id = destinationPath.getTopicId();
        JobDbEntity job = serviceProvider.getJobService().getJobById(id);
        return serviceProvider.getPermissionCheckerService().hasViewPermission(job, user);
    }
}
