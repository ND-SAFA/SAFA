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
     * @param project The project entity containing artifacts, traces, name, and decriptions.
     * @return The project and associated entities created.
     * @throws ServerError Throws error if a database violation occurred while creating or updating any entities in
     *                     payload.
     */
    @PostMapping(AppRoutes.Projects.projects)
    @ResponseStatus(HttpStatus.CREATED)
    public ServerResponse createOrUpdateProject(@RequestBody @Valid ProjectAppEntity project) throws ServerError {
        Project payloadProject = Project.fromAppEntity(project);
        ProjectVersion payloadProjectVersion = project.projectVersion;

        ProjectEntities response;
        if (!payloadProject.hasDefinedId()) { // new projects expected to have no projectId or projectVersion
            SafaUser currentUser = safaUserService.getCurrentUser();
            payloadProject.setOwner(currentUser);
            response = this.projectService.createNewProjectWithVersion(payloadProject, payloadProjectVersion, project);
        } else {
            response = this.projectService.updateProjectAtVersion(payloadProject, payloadProjectVersion, project);
        }

        return new ServerResponse(response);
    }

    /**
     * Returns list of all project identifiers present in the database.
     *
     * @return List of project identifiers.
     */
    public ServerResponse getProjects(Authentication authenticatedUser) {
        SafaUser user = safaUserService.getUserFromAuthentication(authenticatedUser);
        return new ServerResponse(this.projectRepository.findByOwner(user));
    @GetMapping(AppRoutes.Projects.projects)
    }

    /**
     * Deletes project with associated projectId.
     *
     * @param projectId UUID of project to delete.
     * @return String with success message.
     * @throws ServerError Throws error if project with associated id is not found.
     */
    @DeleteMapping(AppRoutes.Projects.projectById)
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

    }
}
