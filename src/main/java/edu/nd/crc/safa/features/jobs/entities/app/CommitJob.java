package edu.nd.crc.safa.features.jobs.entities.app;

import java.io.IOException;
import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.errors.entities.db.CommitError;
import edu.nd.crc.safa.features.flatfiles.builder.steps.CommitStep;
import edu.nd.crc.safa.features.jobs.entities.IJobStep;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.jobs.logging.JobLogger;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.utilities.CommitJobUtility;
import edu.nd.crc.safa.utilities.ProjectOwner;

import lombok.AccessLevel;
import lombok.Getter;
import lombok.Setter;

/**
 * The worker responsible for providing method implementations for
 * the steps to create projects.
 */
public abstract class CommitJob extends AbstractJob {
    private final boolean deleteProjectOnFail;
    @Getter(AccessLevel.PROTECTED)
    private final SafaUser user;
    @Setter
    @Getter
    private ProjectCommitDefinition projectCommitDefinition;
    @Setter
    private ProjectVersion createdProjectVersion;
    @Setter
    private boolean asCompleteSet = false;

    /**
     * Create a commit job for a project that already exists.
     *
     * @param jobDbEntity             DB entity for this job.
     * @param serviceProvider         Service provider
     * @param projectCommitDefinition The project commit all changes from this job should go into
     */
    protected CommitJob(SafaUser user,
                        JobDbEntity jobDbEntity,
                        ServiceProvider serviceProvider,
                        ProjectCommitDefinition projectCommitDefinition,
                        boolean deleteProjectOnFail) {
        super(jobDbEntity, serviceProvider);
        this.deleteProjectOnFail = deleteProjectOnFail;
        this.user = user;
        projectCommitDefinition.setUser(user);
        setProjectCommitDefinition(projectCommitDefinition);
    }

    @IJobStep(value = "Committing Entities", position = -2)
    public void commitArtifactsAndTraceLinks(JobLogger logger) throws SafaError {
        projectCommitDefinition.setUser(getUser());
        List<CommitError> errors = CommitStep.performCommit(
            getServiceProvider(),
            projectCommitDefinition,
            this.asCompleteSet
        );

        if (!errors.isEmpty()) {
            logger.log("### **The following errors were encountered while "
                + "attempting to commit the project changes**");

            for (int i = 0; i < errors.size(); ++i) {
                logger.log((i + 1) + ") " + errors.get(i).getDescription());
            }
        }
    }

    /**
     * @return Returns the project version that this commit is being applied to.
     */
    public ProjectVersion getProjectVersion() {
        return this.projectCommitDefinition.getCommitVersion();
    }

    /**
     * @return Returns the ID of project version commit was applied to.
     */
    @Override
    protected UUID getCompletedEntityId() {
        assertProjectVersionIsSet();
        return getProjectVersion().getVersionId();
    }

    /**
     * Deletes project on fail if flag is set.
     *
     * @param error The error that caused the job to fail.
     * @throws RuntimeException If a problem occurs while saving.
     * @throws IOException      If a problem occurs while logging.
     */
    @Override
    protected void jobFailed(Exception error) throws RuntimeException, IOException {
        if (this.deleteProjectOnFail && createdProjectVersion != null) {
            this.getDbLogger().log("Job failed, deleting job.");
            Project project = createdProjectVersion.getProject();
            getServiceProvider().getProjectService().deleteProject(getUser(), project);
        }
    }

    /**
     * Links project with commit job.
     *
     * @param project The project to associated with job.
     */
    protected void linkProjectToJob(Project project) {
        JobDbEntity job = this.getJobDbEntity();
        job.setProject(project);
        this.getServiceProvider().getJobRepository().save(job);
    }

    /**
     * Links the project referenced in commit to job.
     */
    @Override
    protected void beforeJob() {
        ProjectVersion projectVersion = this.projectCommitDefinition.getCommitVersion();
        if (projectVersion != null) {
            Project project = projectVersion.getProject();
            linkProjectToJob(project);
        }
    }

    /**
     * Creates new project and commit associated with project.
     *
     * @param name        The name of the project.
     * @param description The description of project.
     */
    protected void createProjectAndCommit(ProjectOwner owner, String name, String description) {
        ProjectCommitDefinition commit = CommitJobUtility.createProject(this.getServiceProvider(), owner, name,
            description, getUser());
        setProjectCommitDefinition(commit);
        setCreatedProjectVersion(commit.getCommitVersion());
    }

    /**
     * Asserts that project version has been set.
     */
    private void assertProjectVersionIsSet() {
        if (this.projectCommitDefinition == null || this.projectCommitDefinition.getCommitVersion() == null) {
            throw new NullPointerException("Project version is not set.");
        }
    }
}
