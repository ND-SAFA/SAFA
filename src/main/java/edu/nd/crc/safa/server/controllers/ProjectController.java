package edu.nd.crc.safa.server.controllers;

import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;
import javax.validation.Valid;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.api.ProjectEntities;
import edu.nd.crc.safa.server.entities.api.ProjectMembershipRequest;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.api.ServerResponse;
import edu.nd.crc.safa.server.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.server.entities.app.ProjectMemberAppEntity;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectMembership;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.ProjectRepository;
import edu.nd.crc.safa.server.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.services.ProjectService;
import edu.nd.crc.safa.server.services.RevisionNotificationService;

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

    private final ProjectService projectService;
    private final RevisionNotificationService revisionNotificationService;

    @Autowired
    public ProjectController(ProjectRepository projectRepository,
                             ProjectVersionRepository projectVersionRepository,
                             ResourceBuilder resourceBuilder,
                             ProjectService projectService,
                             RevisionNotificationService revisionNotificationService) {
        super(projectRepository, projectVersionRepository, resourceBuilder);
        this.projectService = projectService;
        this.revisionNotificationService = revisionNotificationService;
    }

    /**
     * Creates or updates project given creating or updating defined entities (e.g. artifacts, traces). Note, artifacts
     * not specified are assumed to be removed if version is specified..
     *
     * @param project The project entity containing artifacts, traces, name, and decriptions.
     * @return The project and associated entities created.
     * @throws SafaError Throws error if a database violation occurred while creating or updating any entities in
     *                   payload.
     */
    @PostMapping(AppRoutes.Projects.projects)
    @ResponseStatus(HttpStatus.CREATED)
    public ServerResponse createOrUpdateProject(@RequestBody @Valid ProjectAppEntity project) throws SafaError {
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
     * @throws SafaError Throws error if project with associated id is not found.
     */
    @DeleteMapping(AppRoutes.Projects.deleteProjectById)
    @ResponseStatus(HttpStatus.OK)
    public ServerResponse deleteProject(@PathVariable UUID projectId) throws SafaError {
        Project project = this.resourceBuilder.fetchProject(projectId).withEditProject();
        this.projectRepository.delete(project);
        return new ServerResponse("Project deleted successfully");
    }

    /**
     * Adds specified user account with given email to project assigned with
     * given role.
     *
     * @param projectId The UUID of the project which the member is being added to.
     * @param request   The request containing project, member to add, and their given role.
     */
    @PostMapping(AppRoutes.Projects.addProjectMember)
    public void addOrUpdateProjectMembership(@PathVariable UUID projectId,
                                             @RequestBody ProjectMembershipRequest request)
        throws SafaError {
        Project project = this.resourceBuilder.fetchProject(projectId).withViewProject();
        this.projectService.addOrUpdateProjectMembership(project,
            request.getMemberEmail(),
            request.getProjectRole());
        this.revisionNotificationService.broadUpdateProjectMessage(project, "members");
    }

    /**
     * Returns all members belonging to given project.
     *
     * @param projectId The project whose members are being retrieved.
     * @return ServerResponse containing list of project members ships
     */
    @GetMapping(AppRoutes.Projects.getProjectMembers)
    public ServerResponse getProjectMembers(@PathVariable UUID projectId) throws SafaError {
        Project project = this.resourceBuilder.fetchProject(projectId).withViewProject();
        List<ProjectMemberAppEntity> projectMemberships = this.projectService.getProjectMembers(project)
            .stream()
            .map(ProjectMemberAppEntity::new)
            .collect(Collectors.toList());
        return new ServerResponse(projectMemberships);
    }

    /**
     * Deletes project membership effectively removing user from
     * associated project
     *
     * @param projectMembershipId ID of the membership linking user and project.
     */
    @DeleteMapping(AppRoutes.Projects.deleteProjectMembership)
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteProjectMemberById(@PathVariable UUID projectMembershipId) throws SafaError {
        //TODO: Check for project permission before deleting.
        ProjectMembership projectMembership = this.projectService.deleteProjectMembershipById(projectMembershipId);
        if (projectMembership != null) {
            this.revisionNotificationService.broadUpdateProjectMessage(projectMembership.getProject(), "members");
        }
    }
}
