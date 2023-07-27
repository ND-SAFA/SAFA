package edu.nd.crc.safa.features.jobs.entities.app;

import java.io.IOException;
import java.util.UUID;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommit;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.entities.IJobStep;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.services.ProjectService;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.ProjectChanger;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.features.versions.services.VersionService;

import lombok.Getter;
import lombok.Setter;

/**
 * The worker responsible for providing method implementations for
 * the steps to create projects.
 */
public abstract class CommitJob extends AbstractJob {

    private final ProjectService projectService;
    private final VersionService versionService;
    @Setter
    @Getter
    private ProjectCommit projectCommit;
    private ProjectVersion createdProjectVersion;

    /**
     * Create a commit job for a project that already exists.
     *
     * @param jobDbEntity     DB entity for this job.
     * @param serviceProvider Service provider
     * @param projectCommit   The project commit all changes from this job should go into
     */
    protected CommitJob(JobDbEntity jobDbEntity, ServiceProvider serviceProvider, ProjectCommit projectCommit) {
        super(jobDbEntity, serviceProvider);
        this.projectService = serviceProvider.getProjectService();
        this.versionService = serviceProvider.getVersionService();
        this.projectCommit = projectCommit;
    }

    protected CommitJob(JobDbEntity jobDbEntity, ServiceProvider serviceProvider) {
        super(jobDbEntity, serviceProvider);
        this.projectService = serviceProvider.getProjectService();
        this.versionService = serviceProvider.getVersionService();

        this.projectCommit = null;
    }

    @IJobStep(value = "Committing Entities", position = -2)
    public void commitArtifactsAndTraceLinks() throws SafaError {
        assertProjectVersionIsSet();
        this.getDbLogger().log(this.projectCommit.getSummary());
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

    /**
     * Creates a new project.
     *
     * @param owner       The owner of the project.
     * @param name        The name of the project.
     * @param description The description of the project.
     * @return A newly created project version.
     */
    protected ProjectVersion createProject(SafaUser owner, String name, String description) {
        Project project = new Project(name, description);
        projectService.saveProjectWithUserAsOwner(project, owner);

        this.createdProjectVersion = versionService.createInitialProjectVersion(project);
        projectCommit = new ProjectCommit(createdProjectVersion, false);
        return createdProjectVersion;
    }

    @Override
    protected void jobFailed(Exception error) throws RuntimeException, IOException {
        if (createdProjectVersion != null) {
            this.getDbLogger().log("Job failed, deleting job.");
            projectService.deleteProject(createdProjectVersion.getProject());
        }
    }

    protected void setCreatedProjectVersion(ProjectVersion projectVersion) {
        this.createdProjectVersion = projectVersion;
    }
}
