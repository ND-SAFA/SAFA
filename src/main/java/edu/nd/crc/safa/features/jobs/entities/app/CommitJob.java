package edu.nd.crc.safa.features.jobs.entities.app;

import java.util.UUID;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.entities.IJobStep;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.versions.ProjectChanger;

import lombok.Setter;

/**
 * The worker responsible for providing method implementations for
 * the steps to create projects.
 */
public abstract class CommitJob extends AbstractJob {

    @Setter
    private ProjectCommit projectCommit;

    /**
     * Create a commit job for a project that already exists.
     *
     * @param jobDbEntity DB entity for this job.
     * @param serviceProvider Service provider
     * @param projectCommit The project commit all changes from this job should go into
     */
    protected CommitJob(JobDbEntity jobDbEntity,
                        ServiceProvider serviceProvider,
                        ProjectCommit projectCommit) {
        super(jobDbEntity, serviceProvider);
        this.projectCommit = projectCommit;
    }

    protected CommitJob(JobDbEntity jobDbEntity,
                        ServiceProvider serviceProvider) {
        super(jobDbEntity, serviceProvider);
        this.projectCommit = null;
    }

    @IJobStep(value = "Committing Entities", position = -2)
    public void commitArtifactsAndTraceLinks() throws SafaError {
        assertProjectVersionIsSet();
        ProjectChanger projectChanger = new ProjectChanger(projectCommit.getCommitVersion(), serviceProvider);
        projectChanger.commitAsUser(projectCommit, getJobDbEntity().getUser());
    }

    private void assertProjectVersionIsSet() {
        if (this.projectCommit == null || this.projectCommit.getCommitVersion() == null) {
            throw new NullPointerException("Project version is not set.");
        }
    }

    @Override
    protected UUID getCompletedEntityId() {
        assertProjectVersionIsSet();
        return projectCommit.getCommitVersion().getVersionId();
    }
}
