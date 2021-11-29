package edu.nd.crc.safa.server.controllers;

import java.util.Optional;
import java.util.UUID;
import javax.validation.Valid;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.authentication.SafaUserService;
import edu.nd.crc.safa.server.entities.api.ProjectEntities;
import edu.nd.crc.safa.server.entities.api.ServerError;
import edu.nd.crc.safa.server.entities.api.ServerResponse;
import edu.nd.crc.safa.server.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.SafaUser;
import edu.nd.crc.safa.server.repositories.ProjectRepository;
import edu.nd.crc.safa.server.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.services.ProjectService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

/**
 * Provides endpoints for creating and updating project entities via JSON.
 */
@RestController
public class ProjectController extends BaseController {

    private final SafaUserService safaUserService;
    private final ProjectService projectService;

    @Autowired
    public ProjectController(ProjectRepository projectRepository,
                             ProjectVersionRepository projectVersionRepository,
                             SafaUserService safaUserService,
                             ProjectService projectService) {
        super(projectRepository, projectVersionRepository);
        this.safaUserService = safaUserService;
        this.projectService = projectService;
    }

    /**
     * Creates or updates project given creating or updating defined entities (e.g. artifacts, traces). Note, artifacts
     * not specified are assumed to be removed if version is specified..
     *
     * @param project           The project entity containing artifacts, traces, name, and decriptions.
     * @param authenticatedUser The authorized user accessing this endpoint.
     * @return The project and associated entities created.
     * @throws ServerError Throws error if a database violation occurred while creating or updating any entities in
     *                     payload.
     */
    @PostMapping(AppRoutes.projects)
    @ResponseStatus(HttpStatus.CREATED)
    public ServerResponse createOrUpdateProject(@RequestBody @Valid ProjectAppEntity project,
                                                Authentication authenticatedUser) throws ServerError {
        Project payloadProject = Project.fromAppEntity(project);
        ProjectVersion payloadProjectVersion = project.projectVersion;

        ProjectEntities response;
        if (!payloadProject.hasDefinedId()) { // new projects expected to have no projectId or projectVersion
            SafaUser owner = safaUserService.getUserFromAuthentication(authenticatedUser);
            payloadProject.setOwner(owner);
            response = createNewProjectWithVersion(payloadProject, payloadProjectVersion, project);
        } else {
            response = updateProjectAtVersion(payloadProject, payloadProjectVersion, project);
        }

        return new ServerResponse(response);
    }

    /**
     * Returns list of all project identifiers present in the database.
     *
     * @param authenticatedUser The authorized user accessing this endpoint.
     * @return List of project identifiers.
     */
    @GetMapping(AppRoutes.projects)
    public ServerResponse getProjects(Authentication authenticatedUser) {
        SafaUser user = safaUserService.getUserFromAuthentication(authenticatedUser);
        return new ServerResponse(this.projectRepository.findByOwner(user));
    }

    /**
     * Deletes project with associated projectId.
     *
     * @param projectId UUID of project to delete.
     * @return String with success message.
     * @throws ServerError Throws error if project with associated id is not found.
     */
    @DeleteMapping(AppRoutes.projectById)
    @ResponseStatus(HttpStatus.OK)
    public ServerResponse deleteProject(@PathVariable String projectId) throws ServerError {
        Optional<Project> projectQuery = this.projectRepository.findById(UUID.fromString(projectId));
        if (projectQuery.isPresent()) {
            this.projectRepository.delete(projectQuery.get());
            return new ServerResponse("Project deleted successfully");
        } else {
            throw new ServerError("Could not find project with id" + projectId);
        }
    }

    private ProjectEntities updateProjectAtVersion(Project project,
                                                   ProjectVersion projectVersion,
                                                   ProjectAppEntity payload) throws ServerError {
        ProjectEntities response;
        Project persistentProject = this.projectRepository.findByProjectId(project.getProjectId());
        persistentProject.setName(project.getName());
        persistentProject.setDescription(project.getDescription());
        //TODO: Update owner here.
        this.projectRepository.save(persistentProject);
        //TODO: Update traces
        if (projectVersion == null) {
            if ((payload.artifacts != null
                && payload.artifacts.size() > 0)) {
                throw new ServerError("Cannot update artifacts because project version not defined");
            }
            response = new ProjectEntities(payload, null, null, null);
        } else if (!projectVersion.hasValidId()) {
            throw new ServerError("Invalid Project version: must have a valid ID.");
        } else if (!projectVersion.hasValidVersion()) {
            throw new ServerError("Invalid Project version: must contain positive major, minor, and revision "
                + "numbers.");
        } else {
            projectVersion.setProject(project);
            this.projectVersionRepository.save(projectVersion);
            response = this.projectService.updateProject(projectVersion, payload);
        }
        return response;
    }

    private ProjectEntities createNewProjectWithVersion(
        Project project,
        ProjectVersion projectVersion,
        ProjectAppEntity payload) throws ServerError {
        ProjectEntities entityCreationResponse;
        if (projectVersion != null
            && projectVersion.hasValidVersion()
            && projectVersion.hasValidId()) {
            throw new ServerError("Invalid ProjectVersion: cannot be defined when creating a new project.");
        }
        this.projectRepository.save(project);
        projectVersion = createProjectVersion(project);
        entityCreationResponse = this.projectService.saveProjectEntitiesToVersion(projectVersion, payload.getArtifacts(), payload.getTraces());
        return entityCreationResponse;
    }
}
