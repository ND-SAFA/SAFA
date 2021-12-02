package edu.nd.crc.safa.builders;

import java.util.UUID;

import edu.nd.crc.safa.server.entities.api.ServerError;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.ProjectRepository;
import edu.nd.crc.safa.server.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.services.PermissionService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

/**
 * Responsible for fetching project and versions and asserting that
 * the current user has permissions to operate on it.
 */
@Component
public class ResourceBuilder {
    Project project;
    ProjectVersion projectVersion;

    ProjectRepository projectRepository;
    ProjectVersionRepository projectVersionRepository;
    PermissionService permissionService;

    @Autowired
    public ResourceBuilder(ProjectRepository projectRepository,
                           ProjectVersionRepository projectVersionRepository,
                           PermissionService permissionService) {
        this.project = null;
        this.projectVersion = null;
        this.projectRepository = projectRepository;
        this.projectVersionRepository = projectVersionRepository;
        this.permissionService = permissionService;
    }

    public ResourceBuilder fetchProject(UUID projectId) {
        this.project = this.projectRepository.findByProjectId(projectId);
        return this;
    }

    public ResourceBuilder getProjectVersion(UUID versionId) {
        this.projectVersion = this.projectVersionRepository.findByVersionId(versionId);
        return this;
    }

    public Project withViewProject() throws ServerError {
        this.permissionService.requireViewPermission(project);
        return this.project;
    }

    public Project withEditProject() throws ServerError {
        this.permissionService.requireViewPermission(project);
        return this.project;
    }

    public ProjectVersion withViewVersion() throws ServerError {
        this.permissionService.requireViewPermission(projectVersion.getProject());
        return projectVersion;
    }

    public ProjectVersion withEditVersion() throws ServerError {
        this.permissionService.requireEditPermission(projectVersion.getProject());
        return projectVersion;
    }
}
