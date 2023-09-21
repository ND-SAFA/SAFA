package edu.nd.crc.safa.features.jobs.entities.app;

import java.io.IOException;
import java.util.UUID;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.entities.IJobStep;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.ProjectChanger;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.utilities.CommitJobUtility;

import lombok.Getter;
import lombok.Setter;

/**
 * The worker responsible for providing method implementations for
 * the steps to create projects.
 */
public abstract class CommitJob extends AbstractJob {
    @Setter
    @Getter
    private ProjectCommitDefinition projectCommitDefinition;
    @Setter
    private ProjectVersion createdProjectVersion;

    protected CommitJob(JobDbEntity jobDbEntity, ServiceProvider serviceProvider) {
        super(jobDbEntity, serviceProvider);
        this.projectCommitDefinition = new ProjectCommitDefinition();
    }

    /**
     * Create a commit job for a project that already exists.
     *
     * @param jobDbEntity             DB entity for this job.
     * @param serviceProvider         Service provider
     * @param projectCommitDefinition The project commit all changes from this job should go into
     */
    protected CommitJob(JobDbEntity jobDbEntity, ServiceProvider serviceProvider,
                        ProjectCommitDefinition projectCommitDefinition) {
        this(jobDbEntity, serviceProvider);
        setProjectCommitDefinition(projectCommitDefinition);
    }

    @Override
    public void beforeJob() {
        ProjectVersion projectVersion = this.projectCommitDefinition.getCommitVersion();
        Project project = projectVersion.getProject();
        JobDbEntity job = this.getJobDbEntity();
        job.setProject(project);
        this.getServiceProvider().getJobRepository().save(job);
    }

    @IJobStep(value = "Committing Entities", position = -2)
    public void commitArtifactsAndTraceLinks() throws SafaError {
        assertProjectVersionIsSet();
        this.getDbLogger().log(this.projectCommitDefinition.getSummary());
        ProjectChanger projectChanger = new ProjectChanger(projectCommitDefinition.getCommitVersion(),
            this.getServiceProvider());
        projectChanger.commitAsUser(projectCommitDefinition, getJobDbEntity().getUser());
    }

    private void assertProjectVersionIsSet() {
        if (this.projectCommitDefinition == null || this.projectCommitDefinition.getCommitVersion() == null) {
            throw new NullPointerException("Project version is not set.");
        }
    }

    @Override
    protected UUID getCompletedEntityId() {
        assertProjectVersionIsSet();
        return projectCommitDefinition.getCommitVersion().getVersionId();
    }

    @Override
    protected void jobFailed(Exception error) throws RuntimeException, IOException {
        if (createdProjectVersion != null) {
            this.getDbLogger().log("Job failed, deleting job.");
            getServiceProvider().getProjectService().deleteProject(createdProjectVersion.getProject());
        }
    }

    protected void createProjectAndCommit(String projectName, String description) {
        ProjectCommitDefinition commit = CommitJobUtility.createProject(this.getServiceProvider(), projectName,
            description);
        setProjectCommitDefinition(commit);
        setCreatedProjectVersion(commit.getCommitVersion());
    }

    public ProjectVersion getProjectVersion() {
        return this.projectCommitDefinition.getCommitVersion();
    }
}
