package edu.nd.crc.safa.features.jobs.entities.app;

import java.util.UUID;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.entities.IJobStep;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.versions.ProjectChanger;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

/**
 * The worker responsible for providing method implementations for
 * the steps to create projects.
 */
public abstract class CommitJob extends AbstractJob {
    /**
     * The project version of the
     */
    protected ProjectCommit projectCommit;
    /**
     * The entities created during job.
     */
    ProjectAppEntity projectAppEntity;
    /**
     * The service used for creating entities.
     */
    ProjectChanger projectChanger;

    public CommitJob(JobDbEntity jobDbEntity,
                     ServiceProvider serviceProvider,
                     ProjectCommit projectCommit) {
        super(jobDbEntity, serviceProvider);
        ProjectVersion projectVersion = projectCommit.getCommitVersion();
        if (projectVersion == null) {
            throw new IllegalArgumentException("Project version is null!");
        }
        this.projectCommit = projectCommit;
        this.projectChanger = new ProjectChanger(projectVersion, serviceProvider);
    }

    @IJobStep(value = "Committing Entities", position = -2)
    public void commitArtifactsAndTraceLinks() throws SafaError {
        projectChanger.commit(projectCommit);
    }

    @Override
    protected UUID getCompletedEntityId() {
        return projectCommit.getCommitVersion().getVersionId();
    }
}
