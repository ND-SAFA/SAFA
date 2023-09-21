package edu.nd.crc.safa.utilities;

import java.io.IOException;

import edu.nd.crc.safa.features.commits.entities.app.ProjectCommitDefinition;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.entities.app.CommitJob;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.services.ProjectService;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.services.SafaUserService;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.features.versions.services.VersionService;

public class CommitJobUtility {

    /**
     * Creates a new project.
     *
     * @param serviceProvider Provides access to services.
     * @param name            The name of the project.
     * @param description     The description of the project.
     * @return A newly created project version.
     */
    public static ProjectCommitDefinition createProject(ServiceProvider serviceProvider, String name,
                                                        String description) {
        ProjectService projectService = serviceProvider.getProjectService();
        VersionService versionService = serviceProvider.getVersionService();
        SafaUserService userService = serviceProvider.getSafaUserService();

        SafaUser owner = userService.getCurrentUser();
        Project project = projectService.createProject(name, description, owner);
        ProjectVersion projectVersion = versionService.createInitialProjectVersion(project);
        ProjectCommitDefinition projectCommitDefinition = new ProjectCommitDefinition(projectVersion, false);
        return projectCommitDefinition;
    }

    public static void deleteCommitProject(CommitJob commitJob) throws IOException {
        ProjectService projectService = commitJob.getServiceProvider().getProjectService();
        projectService.deleteProject(commitJob.getProjectVersion().getProject());
    }
}
