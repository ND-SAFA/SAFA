package edu.nd.crc.safa.authentication.builders;

import java.util.UUID;

import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.repositories.ProjectRepository;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.services.PermissionCheckerService;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.features.versions.repositories.ProjectVersionRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

/**
 * Responsible for fetching project and versions and asserting that
 * the current user has permissions to operate on it.
 */
@Component
public class ResourceBuilder {
    private final ProjectRepository projectRepository;
    private final ProjectVersionRepository projectVersionRepository;
    private final PermissionCheckerService permissionCheckerService;

    Project project;
    ProjectVersion projectVersion;

    @Autowired
    public ResourceBuilder(ProjectRepository projectRepository,
                           ProjectVersionRepository projectVersionRepository,
                           PermissionCheckerService permissionCheckerService) {
        this.project = null;
        this.projectVersion = null;
        this.projectRepository = projectRepository;
        this.projectVersionRepository = projectVersionRepository;
        this.permissionCheckerService = permissionCheckerService;
    }

    public ResourceBuilder fetchProject(UUID projectId) throws SafaError {
        this.project = this.projectRepository.findByProjectId(projectId);
        if (this.project == null) {
            throw new SafaError("Unable to find project with ID: %s.", projectId);
        }
        return this;
    }

    public ResourceBuilder fetchVersion(UUID versionId) throws SafaError {
        this.projectVersion = this.projectVersionRepository.findByVersionId(versionId);
        if (this.projectVersion == null) {
            throw new SafaError("Unable to find project version with id: %s.", versionId);
        }
        return this;
    }

    public ResourceBuilder setProject(Project project) {
        this.project = project;
        return this;
    }

    public Project withOwnProject() throws SafaError {
        this.permissionCheckerService.requireOwnerPermission(project);
        return this.project;
    }

    public Project withOwnProjectAs(SafaUser user) throws SafaError {
        this.permissionCheckerService.requireOwnerPermission(project, user);
        return this.project;
    }

    public Project withViewProject() throws SafaError {
        this.permissionCheckerService.requireViewPermission(project);
        return this.project;
    }

    public Project withViewProjectAs(SafaUser user) throws SafaError {
        this.permissionCheckerService.requireViewPermission(project, user);
        return this.project;
    }

    public Project withEditProject() {
        this.permissionCheckerService.requireEditPermission(project);
        return this.project;
    }

    public Project withEditProjectAs(SafaUser user) {
        this.permissionCheckerService.requireEditPermission(project, user);
        return this.project;
    }

    public ProjectVersion withViewVersion() {
        this.permissionCheckerService.requireViewPermission(projectVersion.getProject());
        return projectVersion;
    }

    public ProjectVersion withViewVersionAs(SafaUser user) {
        this.permissionCheckerService.requireViewPermission(projectVersion.getProject(), user);
        return projectVersion;
    }

    public ProjectVersion withEditVersion() {
        this.permissionCheckerService.requireEditPermission(projectVersion.getProject());
        return projectVersion;
    }

    public ProjectVersion withEditVersionAs(SafaUser user) {
        this.permissionCheckerService.requireEditPermission(projectVersion.getProject(), user);
        return projectVersion;
    }
}
