package edu.nd.crc.safa.features.notifications.builders;

import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.IUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

/**
 * Used to build multiple changes into an entity change.
 */
public class EntityChangeBuilder {
    /**
     * Creates change builder for project.
     *
     * @param user    The user initiating the change.
     * @param project The project being updated.
     * @return The change builder.
     */
    public static ProjectChangeBuilder create(IUser user, Project project) {
        return new ProjectChangeBuilder(user, project);
    }

    /**
     * Creates change builder for project version..
     *
     * @param user           The user initiating the change.
     * @param projectVersion The project version being updated.
     * @return The change builder.
     */
    public static ProjectVersionChangeBuilder create(IUser user, ProjectVersion projectVersion) {
        return new ProjectVersionChangeBuilder(user, projectVersion);
    }

    /**
     * Creates change builder for job.
     *
     * @param user The user initiating the change.
     * @param job  The job being updated.
     * @return The change builder.
     */
    public static JobChangeBuilder create(IUser user, JobDbEntity job) {
        return new JobChangeBuilder(user, job);
    }

    /**
     * Creates change builder for user.
     *
     * @param user The user to send change to.
     * @return The change builder.
     */
    public static UserChangeBuilder create(IUser user) {
        return new UserChangeBuilder(user);
    }
}
