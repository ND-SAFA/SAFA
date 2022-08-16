package edu.nd.crc.safa.features.versions.controllers;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;
import edu.nd.crc.safa.features.versions.services.VersionService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

/**
 * Provides endpoints for retrieving, creating, and deleting project versions.
 */
@RestController
public class VersionController extends BaseController {

    VersionService versionService;

    @Autowired
    public VersionController(ResourceBuilder resourceBuilder,
                             ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
        this.versionService = serviceProvider.getVersionService();
    }

    /**
     * Returns list of versions in project associated with given projectId.
     *
     * @param projectId UUID of project whose versions are returned.
     * @return List of project versions associated with project.
     * @throws SafaError Throws error if project with ID is not found.
     */
    @GetMapping(AppRoutes.Versions.GET_VERSIONS)
    public List<ProjectVersion> getVersions(@PathVariable UUID projectId) throws SafaError {
        Project project = this.resourceBuilder.fetchProject(projectId).withViewProject();
        return this.versionService.getProjectVersions(project);
    }

    /**
     * Returns the greatest version of associated project.
     *
     * @param projectId UUID identifying project whose version is returned.
     * @return Most up-to-date project version.
     * @throws SafaError Throws error if not project if found with associated id.
     */
    @GetMapping(AppRoutes.Versions.GET_CURRENT_VERSION)
    public ProjectVersion getCurrentVersion(@PathVariable UUID projectId) throws SafaError {
        Project project = this.resourceBuilder.fetchProject(projectId).withViewProject();
        return this.versionService.getCurrentVersion(project);
    }

    /**
     * Creates a new major version from the current project version.
     *
     * @param projectId UUID of project whose version will be created for.
     * @return Project version created.
     * @throws SafaError Throws error if no project found with given id.
     */
    @PostMapping(AppRoutes.Versions.CREATE_NEW_MAJOR_VERSION)
    @ResponseStatus(HttpStatus.CREATED)
    public ProjectVersion createNewMajorVersion(@PathVariable UUID projectId) throws SafaError {
        Project project = this.resourceBuilder.fetchProject(projectId).withEditProject();
        return versionService.createNewMajorVersion(project);
    }

    /**
     * Creates a new minor version of the current project version.
     *
     * @param projectId UUID of project whose version will be created for.
     * @return Project version created.
     * @throws SafaError Throws error if no project found with given id.
     */
    @PostMapping(AppRoutes.Versions.CREATE_NEW_MINOR_VERSION)
    @ResponseStatus(HttpStatus.CREATED)
    public ProjectVersion createNewMinorVersion(@PathVariable UUID projectId) throws SafaError {
        Project project = this.resourceBuilder.fetchProject(projectId).withEditProject();
        return versionService.createNewMinorVersion(project);
    }

    /**
     * Creates a new revision of the current project version.
     *
     * @param projectId UUID of project whose version will be created for.
     * @return Project version created.
     * @throws SafaError Throws error if no project found with given id.
     */
    @PostMapping(AppRoutes.Versions.CREATE_NEW_REVISION_VERSION)
    @ResponseStatus(HttpStatus.CREATED)
    public ProjectVersion createNewRevisionVersion(@PathVariable UUID projectId) throws SafaError {
        Project project = this.resourceBuilder.fetchProject(projectId).withEditProject();
        return versionService.createNextRevision(project);
    }

    /**
     * Deletes version associated with given version id.
     *
     * @param versionId UUID identifying version to delete.
     * @throws SafaError Throws error if not version is associated with given id.
     */
    @DeleteMapping(AppRoutes.Versions.DELETE_VERSION_BY_ID)
    public void deleteVersion(@PathVariable UUID versionId) throws SafaError {
        ProjectVersion projectVersion = this.resourceBuilder.fetchVersion(versionId).withEditVersion();
        this.serviceProvider.getProjectVersionRepository().delete(projectVersion);
    }
}
