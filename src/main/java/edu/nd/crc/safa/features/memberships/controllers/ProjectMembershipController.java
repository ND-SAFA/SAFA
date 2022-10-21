package edu.nd.crc.safa.features.memberships.controllers;

import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.memberships.entities.api.ProjectMembershipRequest;
import edu.nd.crc.safa.features.memberships.entities.app.ProjectMemberAppEntity;
import edu.nd.crc.safa.features.memberships.entities.db.ProjectMembership;
import edu.nd.crc.safa.features.notifications.builders.EntityChangeBuilder;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;

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

    @Autowired
    public ProjectMembershipController(ResourceBuilder resourceBuilder,
                                       ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
    }

    /**
     * Adds specified user account with given email to project assigned with
     * given role.
     *
     * @param projectId The UUID of the project which the member is being added to.
     * @param request   The request containing project, member to add, and their given role.
     * @return {@link ProjectMembership} Updated project membership.
     */
    @PostMapping(AppRoutes.Projects.Membership.ADD_PROJECT_MEMBER)
    public ProjectMemberAppEntity addOrUpdateProjectMembership(@PathVariable UUID projectId,
                                                               @RequestBody ProjectMembershipRequest request)
        throws SafaError {
        Project project = this.resourceBuilder.fetchProject(projectId).withViewProject();
        ProjectMembership updatedProjectMembership = this.serviceProvider
            .getMemberService()
            .addOrUpdateProjectMembership(project, request.getMemberEmail(), request.getProjectRole());
        this.serviceProvider
            .getNotificationService()
            .broadcastChange(EntityChangeBuilder
                .create(projectId)
                .withMembersUpdate(updatedProjectMembership.getMembershipId()));
        return new ProjectMemberAppEntity(updatedProjectMembership);
    }

    /**
     * Returns all members belonging to given project.
     *
     * @param projectId The project whose members are being retrieved.
     * @return ServerResponse containing list of project members ships
     */
    @GetMapping(AppRoutes.Projects.Membership.GET_PROJECT_MEMBERS)
    public List<ProjectMemberAppEntity> getProjectMembers(@PathVariable UUID projectId) throws SafaError {
        Project project = this.resourceBuilder.fetchProject(projectId).withViewProject();
        return this.serviceProvider
            .getMemberService()
            .getProjectMembers(project)
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
    @DeleteMapping(AppRoutes.Projects.Membership.DELETE_PROJECT_MEMBERSHIP)
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteProjectMemberById(@PathVariable UUID projectMembershipId) throws SafaError {
        ProjectMembership projectMembership = this.serviceProvider
            .getMemberService()
            .getMembershipById(projectMembershipId);

        // Step - Verify last member not being deleted.
        Project project = projectMembership.getProject();
        List<ProjectMembership> projectMemberships = this.serviceProvider.getMemberService().getProjectMembers(project);
        if (projectMemberships.size() == 1) {
            throw new SafaError("Cannot delete last member of project.");
        }

        // Step - Verify user has sufficient permissions
        this.resourceBuilder.setProject(project).withEditProject();

        // Step - Delete membership
        this.serviceProvider.getProjectMembershipRepository().delete(projectMembership);

        // Step - Broadcast change
        this.serviceProvider
            .getNotificationService()
            .broadcastChange(
                EntityChangeBuilder
                    .create(project.getProjectId())
                    .withMembersDelete(projectMembershipId)
            );
    }
}
