package edu.nd.crc.safa.features.notifications.security;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;

/**
 * Topic permission check for projects
 */
public class ProjectTopicPermissionCheck extends MembershipEntityTopicPermissionCheck {
    public ProjectTopicPermissionCheck() {
        super(ProjectPermission.VIEW, id -> ServiceProvider.getInstance().getProjectService().getProjectById(id));
    }
}
