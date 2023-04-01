package edu.nd.crc.safa.features.jobs.entities.app;

import java.io.IOException;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.services.ProjectService;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.features.versions.services.VersionService;

/**
 * <p>Superclass for all jobs that create a new project. Handles cleaning up the
 * project if the job fails</p>
 *
 * <p>Users must create the new project by calling {@link #createProject(String, String)}.</p>
 */
public abstract class ProjectCreationJob extends CommitJob {

    private final ProjectService projectService;
    private final VersionService versionService;

    private ProjectVersion createdProjectVersion;

    protected ProjectCreationJob(JobDbEntity jobDbEntity, ServiceProvider serviceProvider) {
        super(jobDbEntity, serviceProvider);
        this.projectService = serviceProvider.getProjectService();
        this.versionService = serviceProvider.getVersionService();
    }

    /**
     * Creates a new project.
     *
     * @param name The name of the project.
     * @param description The description of the project.
     * @return A newly created project version.
     */
    protected ProjectVersion createProject(String name, String description) {
        Project project = new Project(name, description);
        projectService.saveProjectWithUserAsOwner(project, this.jobDbEntity.getUser());

        createdProjectVersion = versionService.createInitialProjectVersion(project);
        return createdProjectVersion;
    }

    @Override
    protected void jobFailed(Exception error) throws RuntimeException, IOException {
        if (createdProjectVersion != null) {
            projectService.deleteProject(createdProjectVersion.getProject());
        }
    }
}
