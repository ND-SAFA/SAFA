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
import edu.nd.crc.safa.features.memberships.entities.db.UserProjectMembership;
import edu.nd.crc.safa.features.memberships.services.MemberService;
import edu.nd.crc.safa.features.memberships.services.ProjectMembershipService;
import edu.nd.crc.safa.features.notifications.builders.EntityChangeBuilder;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.features.permissions.services.PermissionService;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

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

    private final PermissionService permissionService;
    private final ProjectMembershipService projectMembershipService;

    @Autowired
    public ProjectMembershipController(ResourceBuilder resourceBuilder,
                                       ServiceProvider serviceProvider,
                                       PermissionService permissionService,
                                       ProjectMembershipService projectMembershipService) {
        super(resourceBuilder, serviceProvider);
        this.permissionService = permissionService;
        this.projectMembershipService = projectMembershipService;
    }

    /**
     * Adds specified user account with given email to project assigned with
     * given role.
     *
     * @param projectId The UUID of the project which the member is being added to.
     * @param request   The request containing project, member to add, and their given role.
     * @return {@link UserProjectMembership} Updated project membership.
     */
    @PostMapping(AppRoutes.Projects.Membership.ADD_PROJECT_MEMBER)
    public ProjectMemberAppEntity addOrUpdateProjectMembership(@PathVariable UUID projectId,
                                                               @RequestBody ProjectMembershipRequest request)
        throws SafaError {

        SafaUser user = getServiceProvider().getSafaUserService().getCurrentUser();
        SafaUser userToUpdate = getServiceProvider().getSafaUserService().getUserByEmail(request.getMemberEmail());

        Project project = getResourceBuilder().fetchProject(projectId)
                .withPermission(ProjectPermission.SHARE, user).get();

        UserProjectMembership updatedProjectMembership =
                projectMembershipService.addUserRole(userToUpdate, project, request.getProjectRole());

        getServiceProvider()
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
        SafaUser user = getServiceProvider().getSafaUserService().getCurrentUser();
        Project project = getResourceBuilder().fetchProject(projectId)
                .withPermission(ProjectPermission.VIEW, user).get();
        return projectMembershipService
            .getAllProjectMembers(project)
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
        MemberService memberService = getServiceProvider().getMemberService();

        UserProjectMembership projectMembership = memberService.getMembershipById(projectMembershipId);

        // Step - Verify user has sufficient permissions
        // You can always remove yourself, and you can remove others if you have admin permissions
        Project project = projectMembership.getProject();
        SafaUser user = getServiceProvider().getSafaUserService().getCurrentUser();
        if (!projectMembership.getMember().equals(user)) {
            permissionService.requirePermission(ProjectPermission.SHARE, project, user);
        }

        // Step - Delete membership
        getServiceProvider().getUserProjectMembershipRepository().delete(projectMembership);

        // Step - Broadcast change
        getServiceProvider()
            .getNotificationService()
            .broadcastChange(
                EntityChangeBuilder
                    .create(project.getProjectId())
                    .withMembersDelete(projectMembershipId)
            );
    }
}
