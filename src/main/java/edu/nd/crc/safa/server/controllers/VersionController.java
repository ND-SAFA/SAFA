package edu.nd.crc.safa.server.controllers;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.importer.Puller;
import edu.nd.crc.safa.server.entities.api.ProjectEntities;
import edu.nd.crc.safa.server.entities.api.ServerError;
import edu.nd.crc.safa.server.entities.api.ServerResponse;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.ProjectRepository;
import edu.nd.crc.safa.server.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.services.ProjectRetrievalService;
import edu.nd.crc.safa.server.services.ProjectService;
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

    Puller mPuller;
    VersionService versionService;
    ProjectService projectService;
    ProjectRetrievalService projectRetrievalService;

    @Autowired
    public VersionController(ProjectRepository projectRepository,
                             ProjectVersionRepository projectVersionRepository,
                             ResourceBuilder resourceBuilder,
                             Puller mPuller,
                             VersionService versionService,
                             ProjectService projectService,
                             ProjectRetrievalService projectRetrievalService) {
        super(projectRepository, projectVersionRepository, resourceBuilder);
        this.mPuller = mPuller;
        this.versionService = versionService;
        this.projectService = projectService;
        this.projectRetrievalService = projectRetrievalService;
    }

    /**
     * Returns list of versions in project associated with given projectId.
     *
     * @param projectId UUID of project whose versions are returned.
     * @return List of project versions associated with project.
     * @throws ServerError Throws error if project with ID is not found.
     */
    @GetMapping(AppRoutes.Projects.getVersions)
    public ServerResponse getVersions(@PathVariable UUID projectId) throws ServerError {
        Project project = this.resourceBuilder.fetchProject(projectId).withViewProject();
        List<ProjectVersion> projectVersionList = versionService.getProjectVersions(project);
        return new ServerResponse(projectVersionList);
    }

    /**
     * Returns the greatest version of associated project.
     *
     * @param projectId UUID identifying project whose version is returned.
     * @return Most up-to-date project version.
     * @throws ServerError Throws error if not project if found with associated id.
     */
    @GetMapping(AppRoutes.Projects.getCurrentVersion)
    public ServerResponse getCurrentVersion(@PathVariable UUID projectId) throws ServerError {
        Project project = this.resourceBuilder.fetchProject(projectId).withViewProject();
        ProjectVersion projectVersion = versionService.getCurrentVersion(project);
        return new ServerResponse(projectVersion);
    }

    /**
     * Creates a new major version from the current project version.
     *
     * @param projectId UUID of project whose version will be created for.
     * @return Project version created.
     * @throws ServerError Throws error if no project found with given id.
     */
    @PostMapping(AppRoutes.Projects.createNewMajorVersion)
    @ResponseStatus(HttpStatus.CREATED)
    public ServerResponse createNewMajorVersion(@PathVariable UUID projectId) throws ServerError {
        Project project = this.resourceBuilder.fetchProject(projectId).withEditProject();
        ProjectVersion nextVersion = versionService.createNewMajorVersion(project);
        return new ServerResponse(nextVersion);
    }

    /**
     * Creates a new minor version of the current project version.
     *
     * @param projectId UUID of project whose version will be created for.
     * @return Project version created.
     * @throws ServerError Throws error if no project found with given id.
     */
    @PostMapping(AppRoutes.Projects.createNewMinorVersion)
    @ResponseStatus(HttpStatus.CREATED)
    public ServerResponse createNewMinorVersion(@PathVariable UUID projectId) throws ServerError {
        Project project = this.resourceBuilder.fetchProject(projectId).withEditProject();
        ProjectVersion nextVersion = versionService.createNewMinorVersion(project);
        return new ServerResponse(nextVersion);
    }

    /**
     * Creates a new revision of the current project version.
     *
     * @param projectId UUID of project whose version will be created for.
     * @return Project version created.
     * @throws ServerError Throws error if no project found with given id.
     */
    @PostMapping(AppRoutes.Projects.createNewRevisionVersion)
    @ResponseStatus(HttpStatus.CREATED)
    public ServerResponse createNewRevisionVersion(@PathVariable UUID projectId) throws ServerError {
        Project project = this.resourceBuilder.fetchProject(projectId).withEditProject();
        ProjectVersion nextVersion = versionService.createNextRevision(project);
        return new ServerResponse(nextVersion);
    }

    /**
     * Deletes version associated with given version id.
     *
     * @param versionId UUID identifying version to delete.
     * @return String representing success message.
     * @throws ServerError Throws error if not version is associated with given id.
     */
    @DeleteMapping(AppRoutes.Projects.getVersionById)
    public ServerResponse deleteVersion(@PathVariable UUID versionId) throws ServerError {
        ProjectVersion projectVersion = this.resourceBuilder.getProjectVersion(versionId).withEditVersion();
        this.projectVersionRepository.delete(projectVersion);
        return new ServerResponse("Project version deleted successfully");
    }

    /**
     * Returns a project and associated artifacts at version associated with given id.
     *
     * @param versionId UUID of version whose artifacts and trace links are retrieved.
     * @return ProjectCreationResponse containing artifacts, traces, and warnings of project at version specified.
     * @throws ServerError Throws error if no version is associated with given id.
     */
    @GetMapping(AppRoutes.Projects.getVersionById)
    public ServerResponse getProjectById(@PathVariable UUID versionId) throws ServerError {
        ProjectVersion projectVersion = this.resourceBuilder.getProjectVersion(versionId).withViewVersion();
        ProjectEntities response = this.projectRetrievalService
            .retrieveAndCreateProjectResponse(projectVersion);
        return new ServerResponse(response);
    }
}
