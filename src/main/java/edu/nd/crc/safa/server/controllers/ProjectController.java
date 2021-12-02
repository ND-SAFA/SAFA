package edu.nd.crc.safa.server.controllers;

import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;
import javax.validation.Valid;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.authentication.SafaUserService;
import edu.nd.crc.safa.server.entities.api.ProjectEntities;
import edu.nd.crc.safa.server.entities.api.ProjectMembershipRequest;
import edu.nd.crc.safa.server.entities.api.ServerError;
import edu.nd.crc.safa.server.entities.api.ServerResponse;
import edu.nd.crc.safa.server.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.server.entities.app.ProjectMemberAppEntity;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.ProjectRepository;
import edu.nd.crc.safa.server.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.services.ProjectService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
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
                             ResourceBuilder resourceBuilder,
                             SafaUserService safaUserService,
                             ProjectService projectService) {
        super(projectRepository, projectVersionRepository, resourceBuilder);
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
            response = this.projectService.createNewProjectWithVersion(payloadProject, payloadProjectVersion, project);
        } else {
            this.resourceBuilder.fetchProject(payloadProject.getProjectId()).withEditProject();
            response = this.projectService.updateProjectAtVersion(payloadProject, payloadProjectVersion, project);
        }

        return new ServerResponse(response);
    }

    /**
     * Returns list of all project identifiers present in the database.
     *
     * @return List of project identifiers.
     */
    @GetMapping(AppRoutes.Projects.projects)
    public ServerResponse getProjects() {
        List<Project> userProjects = projectService.getCurrentUserProjects();
        return new ServerResponse(userProjects);
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
    public ServerResponse deleteProject(@PathVariable UUID projectId) throws ServerError {
        Project project = this.resourceBuilder.fetchProject(projectId).withEditProject();
        this.projectRepository.delete(project);
        return new ServerResponse("Project deleted successfully");
    }

    /**
     * Adds specified user account with given email to project assigned with
     * given role.
     *
     * @param request The request containing project, member to add, and their given role.
     */
    @PostMapping(AppRoutes.Projects.addProjectMember)
    public void addProjectMember(@RequestBody ProjectMembershipRequest request) throws ServerError {
        this.projectService.addMemberToProject(request.getProjectId(),
            request.getMemberEmail(),
            request.getProjectRole());
    }

    /**
     * Returns all members belonging to given project.
     *
     * @param projectId The project whose members are being retrieved.
     * @return ServerResponse containing list of project members ships
     */
    @GetMapping(AppRoutes.Projects.getProjectMembers)
    public ServerResponse getProjectMembers(@PathVariable UUID projectId) throws ServerError {
        Project project = this.resourceBuilder.fetchProject(projectId).withViewProject();
        List<ProjectMemberAppEntity> projectMemberships = this.projectService.getProjectMembers(project)
            .stream()
            .map(ProjectMemberAppEntity::new)
            .collect(Collectors.toList());
        return new ServerResponse(projectMemberships);
    }
}
