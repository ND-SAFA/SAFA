package edu.nd.crc.safa.server.controllers;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.ProjectRepository;
import edu.nd.crc.safa.server.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.services.ProjectRetrievalService;
import edu.nd.crc.safa.server.services.VersionService;

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

    private final VersionService versionService;
    private final ProjectRetrievalService projectRetrievalService;

    @Autowired
    public VersionController(ProjectRepository projectRepository,
                             ProjectVersionRepository projectVersionRepository,
                             ResourceBuilder resourceBuilder,
                             VersionService versionService,
                             ProjectRetrievalService projectRetrievalService) {
        super(projectRepository, projectVersionRepository, resourceBuilder);
        this.versionService = versionService;
        this.projectRetrievalService = projectRetrievalService;
    }

    /**
     * Returns list of versions in project associated with given projectId.
     *
     * @param projectId UUID of project whose versions are returned.
     * @return List of project versions associated with project.
     * @throws SafaError Throws error if project with ID is not found.
     */
    @GetMapping(AppRoutes.Projects.getVersions)
    public List<ProjectVersion> getVersions(@PathVariable UUID projectId) throws SafaError {
        Project project = this.resourceBuilder.fetchProject(projectId).withViewProject();
        List<ProjectVersion> projectVersionList = versionService.getProjectVersions(project);
        return projectVersionList;
    }

    /**
     * Returns the greatest version of associated project.
     *
     * @param projectId UUID identifying project whose version is returned.
     * @return Most up-to-date project version.
     * @throws SafaError Throws error if not project if found with associated id.
     */
    @GetMapping(AppRoutes.Projects.getCurrentVersion)
    public ProjectVersion getCurrentVersion(@PathVariable UUID projectId) throws SafaError {
        Project project = this.resourceBuilder.fetchProject(projectId).withViewProject();
        ProjectVersion projectVersion = versionService.getCurrentVersion(project);
        return projectVersion;
    }

    /**
     * Creates a new major version from the current project version.
     *
     * @param projectId UUID of project whose version will be created for.
     * @return Project version created.
     * @throws SafaError Throws error if no project found with given id.
     */
    @PostMapping(AppRoutes.Projects.createNewMajorVersion)
    @ResponseStatus(HttpStatus.CREATED)
    public ProjectVersion createNewMajorVersion(@PathVariable UUID projectId) throws SafaError {
        Project project = this.resourceBuilder.fetchProject(projectId).withEditProject();
        ProjectVersion nextVersion = versionService.createNewMajorVersion(project);
        return nextVersion;
    }

    /**
     * Creates a new minor version of the current project version.
     *
     * @param projectId UUID of project whose version will be created for.
     * @return Project version created.
     * @throws SafaError Throws error if no project found with given id.
     */
    @PostMapping(AppRoutes.Projects.createNewMinorVersion)
    @ResponseStatus(HttpStatus.CREATED)
    public ProjectVersion createNewMinorVersion(@PathVariable UUID projectId) throws SafaError {
        Project project = this.resourceBuilder.fetchProject(projectId).withEditProject();
        ProjectVersion nextVersion = versionService.createNewMinorVersion(project);
        return nextVersion;
    }

    /**
     * Creates a new revision of the current project version.
     *
     * @param projectId UUID of project whose version will be created for.
     * @return Project version created.
     * @throws SafaError Throws error if no project found with given id.
     */
    @PostMapping(AppRoutes.Projects.createNewRevisionVersion)
    @ResponseStatus(HttpStatus.CREATED)
    public ProjectVersion createNewRevisionVersion(@PathVariable UUID projectId) throws SafaError {
        Project project = this.resourceBuilder.fetchProject(projectId).withEditProject();
        ProjectVersion nextVersion = versionService.createNextRevision(project);
        return nextVersion;
    }

    /**
     * Deletes version associated with given version id.
     *
     * @param versionId UUID identifying version to delete.
     * @throws SafaError Throws error if not version is associated with given id.
     */
    @DeleteMapping(AppRoutes.Projects.deleteVersionById)
    public void deleteVersion(@PathVariable UUID versionId) throws SafaError {
        ProjectVersion projectVersion = this.resourceBuilder.fetchVersion(versionId).withEditVersion();
        this.projectVersionRepository.delete(projectVersion);
    }
}
