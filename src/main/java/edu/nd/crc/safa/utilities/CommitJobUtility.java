package edu.nd.crc.safa.utilities;

import java.io.IOException;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.entities.app.CommitJob;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.services.ProjectService;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.features.versions.services.VersionService;

public class CommitJobUtility {

    /**
     * Creates a new project.
     *
     * @param serviceProvider Provides access to services.
     * @param owner           The project owner.
     * @param name            The name of the project.
     * @param description     The description of the project.
     * @return A newly created project version.
     */
    public static ProjectCommitDefinition createProject(ServiceProvider serviceProvider, ProjectOwner owner,
                                                        String name, String description) {
        ProjectService projectService = serviceProvider.getProjectService();
        VersionService versionService = serviceProvider.getVersionService();

        Project project;
        if (owner.getTeam() != null) {
            project = projectService.createProject(name, description, owner.getTeam());
        } else if (owner.getOrganization() != null) {
            project = projectService.createProject(name, description, owner.getOrganization());
        } else {
            project = projectService.createProject(name, description, owner.getUser());
        }

        ProjectVersion projectVersion = versionService.createInitialProjectVersion(project);
        return new ProjectCommitDefinition(projectVersion, false);
    }

    public static void deleteCommitProject(CommitJob commitJob) throws IOException {
        ProjectService projectService = commitJob.getServiceProvider().getProjectService();
        projectService.deleteProject(commitJob.getProjectCommitDefinition().getUser(),
            commitJob.getProjectVersion().getProject());
    }

}
