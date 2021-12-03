package edu.nd.crc.safa.builders;

import java.util.UUID;

import edu.nd.crc.safa.server.entities.api.SafaError;
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

    public ResourceBuilder fetchProject(UUID projectId) throws SafaError {
        this.project = this.projectRepository.findByProjectId(projectId);
        if (this.project == null) {
            throw new SafaError("Unable to find project with id:" + projectId);
        }
        return this;
    }

    public ResourceBuilder fetchVersion(UUID versionId) throws SafaError {
        this.projectVersion = this.projectVersionRepository.findByVersionId(versionId);
        if (this.projectVersion == null) {
            throw new SafaError("Unable to find project version with id:" + versionId);
        }
        return this;
    }

    public Project withViewProject() throws SafaError {
        this.permissionService.requireViewPermission(project);
        return this.project;
    }

    public Project withEditProject() throws SafaError {
        this.permissionService.requireEditPermission(project);
        return this.project;
    }

    public ProjectVersion withViewVersion() throws SafaError {
        this.permissionService.requireViewPermission(projectVersion.getProject());
        return projectVersion;
    }

    public ProjectVersion withEditVersion() throws SafaError {
        this.permissionService.requireEditPermission(projectVersion.getProject());
        return projectVersion;
    }
}
