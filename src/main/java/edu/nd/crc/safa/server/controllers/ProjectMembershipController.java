package edu.nd.crc.safa.server.controllers;

import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.common.AppRoutes;
import edu.nd.crc.safa.server.entities.api.ProjectMembershipRequest;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.project.ProjectEntityTypes;
import edu.nd.crc.safa.server.entities.app.project.ProjectMemberAppEntity;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectMembership;
import edu.nd.crc.safa.server.services.NotificationService;
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
public class ProjectMembershipController extends BaseController {

    private final ProjectService projectService;
    private final NotificationService notificationService;

    @Autowired
    public ProjectMembershipController(ResourceBuilder resourceBuilder,
                                       ProjectService projectService,
                                       NotificationService notificationService) {
        super(resourceBuilder);
        this.projectService = projectService;
        this.notificationService = notificationService;
    }

    /**
     * Adds specified user account with given email to project assigned with
     * given role.
     *
     * @param projectId The UUID of the project which the member is being added to.
     * @param request   The request containing project, member to add, and their given role.
     */
    @PostMapping(AppRoutes.Projects.Membership.addProjectMember)
    public void addOrUpdateProjectMembership(@PathVariable UUID projectId,
                                             @RequestBody ProjectMembershipRequest request)
        throws SafaError {
        Project project = this.resourceBuilder.fetchProject(projectId).withViewProject();
        this.projectService.addOrUpdateProjectMembership(project,
            request.getMemberEmail(),
            request.getProjectRole());
        this.notificationService.broadUpdateProjectMessage(project, ProjectEntityTypes.MEMBERS);
    }

    /**
     * Returns all members belonging to given project.
     *
     * @param projectId The project whose members are being retrieved.
     * @return ServerResponse containing list of project members ships
     */
    @GetMapping(AppRoutes.Projects.Membership.getProjectMembers)
    public List<ProjectMemberAppEntity> getProjectMembers(@PathVariable UUID projectId) throws SafaError {
        Project project = this.resourceBuilder.fetchProject(projectId).withViewProject();
        return this.projectService.getProjectMembers(project)
            .stream()
            .map(ProjectMemberAppEntity::new)
            .collect(Collectors.toList());
    }

    /**
     * Deletes project membership effectively removing user from
     * associated project
     *
     * @param projectMembershipId ID of the membership linking user and project.
     */
    @DeleteMapping(AppRoutes.Projects.Membership.deleteProjectMembership)
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteProjectMemberById(@PathVariable UUID projectMembershipId) throws SafaError {
        //TODO: Check for project permission before deleting.
        ProjectMembership projectMembership = this.projectService.deleteProjectMembershipById(projectMembershipId);
        if (projectMembership != null) {
            this.notificationService.broadUpdateProjectMessage(
                projectMembership.getProject(),
                ProjectEntityTypes.MEMBERS);
        }
    }
}
