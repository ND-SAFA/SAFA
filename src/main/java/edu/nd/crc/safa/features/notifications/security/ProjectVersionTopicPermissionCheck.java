package edu.nd.crc.safa.features.notifications.security;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;

/**
 * Topic permission check for project versions
 */
public class ProjectVersionTopicPermissionCheck extends MembershipEntityTopicPermissionCheck {
    public ProjectVersionTopicPermissionCheck() {
        super(ProjectPermission.VIEW, id -> ServiceProvider.getInstance().getVersionService().getVersionById(id));
    }
}
