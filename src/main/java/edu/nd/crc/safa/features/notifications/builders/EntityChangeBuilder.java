package edu.nd.crc.safa.features.notifications.builders;

import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.IUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

/**
 * Used to build multiple changes into an entity change.
 */
public class EntityChangeBuilder {
    public static ProjectChangeBuilder create(IUser user, Project project) {
        return new ProjectChangeBuilder(user, project);
    }

    public static ProjectVersionChangeBuilder create(IUser user, ProjectVersion projectVersion) {
        return new ProjectVersionChangeBuilder(user, projectVersion);
    }

    public static JobChangeBuilder create(IUser user, JobDbEntity job) {
        return new JobChangeBuilder(user, job);
    }
}
