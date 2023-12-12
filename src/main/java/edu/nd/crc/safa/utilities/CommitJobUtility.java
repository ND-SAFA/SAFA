package edu.nd.crc.safa.utilities;

import java.io.IOException;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.entities.app.CommitJob;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.services.ProjectService;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
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
     * @param user            The user performing the action
     * @return A newly created project version.
     */
    public static ProjectCommitDefinition createProject(ServiceProvider serviceProvider, ProjectOwner owner,
                                                        String name, String description, SafaUser user) {
        ProjectService projectService = serviceProvider.getProjectService();
        VersionService versionService = serviceProvider.getVersionService();

        Project project;
        if (owner.getTeam() != null) {
            project = projectService.createProjectAsUser(name, description, owner.getTeam(), user);
        } else if (owner.getOrganization() != null) {
            project = projectService.createProjectAsUser(name, description, owner.getOrganization(), user);
        } else {
            project = projectService.createProjectAsUser(name, description, owner.getUser(), user);
        }

        ProjectVersion projectVersion = versionService.createInitialProjectVersion(project);
        return new ProjectCommitDefinition(user, projectVersion, false);
    }

    public static void deleteCommitProject(CommitJob commitJob) throws IOException {
        ProjectService projectService = commitJob.getServiceProvider().getProjectService();
        projectService.deleteProject(commitJob.getProjectCommitDefinition().getUser(),
            commitJob.getProjectVersion().getProject());
    }

}
