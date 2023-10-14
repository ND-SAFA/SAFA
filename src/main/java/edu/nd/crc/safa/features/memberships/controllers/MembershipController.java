package edu.nd.crc.safa.features.memberships.controllers;

import static edu.nd.crc.safa.utilities.AssertUtils.assertEqual;

import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.function.Consumer;
import java.util.function.Function;
import java.util.stream.Collectors;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.memberships.entities.db.EntityMembership;
import edu.nd.crc.safa.features.memberships.entities.db.OrganizationMembership;
import edu.nd.crc.safa.features.memberships.entities.db.ProjectMembership;
import edu.nd.crc.safa.features.memberships.entities.db.TeamMembership;
import edu.nd.crc.safa.features.memberships.services.OrganizationMembershipService;
import edu.nd.crc.safa.features.memberships.services.ProjectMembershipService;
import edu.nd.crc.safa.features.memberships.services.TeamMembershipService;
import edu.nd.crc.safa.features.organizations.entities.app.MembershipAppEntity;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.OrganizationRole;
import edu.nd.crc.safa.features.organizations.entities.db.ProjectRole;
import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.organizations.entities.db.TeamRole;
import edu.nd.crc.safa.features.organizations.services.OrganizationService;
import edu.nd.crc.safa.features.organizations.services.TeamService;
import edu.nd.crc.safa.features.permissions.entities.OrganizationPermission;
import edu.nd.crc.safa.features.permissions.entities.Permission;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.features.permissions.entities.TeamPermission;
import edu.nd.crc.safa.features.permissions.services.PermissionService;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.app.SafaItemNotFoundError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.services.ProjectService;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class MembershipController extends BaseController {

    private final OrganizationService organizationService;
    private final ProjectService projectService;
    private final TeamService teamService;

    private final OrganizationMembershipService orgMembershipService;
    private final ProjectMembershipService projectMembershipService;
    private final TeamMembershipService teamMembershipService;

    private final PermissionService permissionService;

    public MembershipController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider,
                                OrganizationService organizationService, ProjectService projectService,
                                TeamService teamService, OrganizationMembershipService orgMembershipService,
                                ProjectMembershipService projectMembershipService,
                                TeamMembershipService teamMembershipService, PermissionService permissionService) {
        super(resourceBuilder, serviceProvider);
        this.organizationService = organizationService;
        this.projectService = projectService;
        this.teamService = teamService;
        this.orgMembershipService = orgMembershipService;
        this.projectMembershipService = projectMembershipService;
        this.teamMembershipService = teamMembershipService;
        this.permissionService = permissionService;
    }

    /**
     * Get all memberships by an entity's ID. An entity can be an organization, a team,
     * or a project.
     *
     * @param entityId The ID of the entity
     * @return All memberships within the entity, if it exists
     */
    @GetMapping(AppRoutes.Memberships.BY_ENTITY_ID)
    public List<MembershipAppEntity> getMembers(@PathVariable UUID entityId) {
        return toAppEntities(
            transformEntity(
                entityId,
                orgMembershipService::getAllMembershipsByOrganization,
                teamMembershipService::getTeamMemberships,
                projectMembershipService::getProjectMembers,
                OrganizationPermission.VIEW,
                TeamPermission.VIEW,
                ProjectPermission.VIEW
            )
        );
    }

    /**
     * Create a new membership within an entity. An entity can be an organization, a team,
     * or a project.
     *
     * @param entityId The ID of the entity
     * @param newMembership The definition of the new membership. Only the email and role fields are read
     * @return The newly created membership
     */
    @PostMapping(AppRoutes.Memberships.BY_ENTITY_ID)
    public MembershipAppEntity createNewMembership(@PathVariable UUID entityId,
                                                   @RequestBody MembershipAppEntity newMembership) {
        SafaUser newMember = getServiceProvider().getSafaUserService().getUserByEmail(newMembership.getEmail());
        return new MembershipAppEntity(
            transformEntity(
                entityId,
                org ->
                    orgMembershipService.addUserRole(newMember, org, OrganizationRole.valueOf(newMembership.getRole())),
                team ->
                    teamMembershipService.addUserRole(newMember, team, TeamRole.valueOf(newMembership.getRole())),
                proj ->
                    projectMembershipService.addUserRole(newMember, proj, ProjectRole.valueOf(newMembership.getRole())),
                OrganizationPermission.EDIT_MEMBERS,
                TeamPermission.EDIT_MEMBERS,
                ProjectPermission.EDIT_MEMBERS
            )
        );
    }

    /**
     * Modify a user membership within an entity. An entity can be an organization, a team,
     * or a project. Note that due to how the back end handles roles, the modified
     * membership will actually be a new membership with a new ID.
     *
     * @param entityId The ID of the entity
     * @param membershipId The ID of the membership to modify
     * @param membership The modified membership definition. Only the role field is used
     * @return The new membership entity
     */
    @PutMapping(AppRoutes.Memberships.BY_ENTITY_ID_AND_MEMBERSHIP_ID)
    public MembershipAppEntity modifyMembership(@PathVariable UUID entityId, @PathVariable UUID membershipId,
                                                @RequestBody MembershipAppEntity membership) {
        return new MembershipAppEntity(
            transformEntity(
                entityId,
                org -> modifyOrgMembership(membershipId, org, membership.getRole()),
                team -> modifyTeamMembership(membershipId, team, membership.getRole()),
                project -> modifyProjectMembership(membershipId, project, membership.getRole()),
                OrganizationPermission.EDIT_MEMBERS,
                TeamPermission.EDIT_MEMBERS,
                ProjectPermission.EDIT_MEMBERS
            )
        );
    }

    /**
     * Delete a membership within an entity. An entity can be an organization, a team,
     * or a project.
     *
     * @param entityId The ID of the entity
     * @param membershipId The ID of the membership to delete
     */
    @DeleteMapping(AppRoutes.Memberships.BY_ENTITY_ID_AND_MEMBERSHIP_ID)
    public void deleteMembership(@PathVariable UUID entityId, @PathVariable UUID membershipId) {
        consumeEntity(
            entityId,
            org -> modifyOrgMembership(membershipId, org, null),
            team -> modifyTeamMembership(membershipId, team, null),
            project -> modifyProjectMembership(membershipId, project, null),
            OrganizationPermission.EDIT_MEMBERS,
            TeamPermission.EDIT_MEMBERS,
            ProjectPermission.EDIT_MEMBERS
        );
    }

    /**
     * Delete all roles for a user within a given entity. An entity can be an organization, a team,
     * or a project. Either userId or userEmail must be supplied. If both are supplied, userId takes
     * precedence.
     *
     * @param entityId the ID of the entity
     * @param userId The ID of the user
     * @param userEmail The email of the user
     */
    @DeleteMapping(AppRoutes.Memberships.BY_ENTITY_ID)
    public void deleteAllMembershipsForUser(@PathVariable UUID entityId, @RequestParam(required = false) UUID userId,
                                            @RequestParam(required = false) String userEmail) {
        SafaUser member;
        if (userId != null) {
            member = getServiceProvider().getSafaUserService().getUserById(userId);
        } else if (userEmail != null) {
            member = getServiceProvider().getSafaUserService().getUserByEmail(userEmail);
        } else {
            throw new SafaError("Must supply either userId or userEmail");
        }

        consumeEntity(
            entityId,
            org -> orgMembershipService.getUserRoles(member, org)
                .forEach(role -> orgMembershipService.removeUserRole(member, org, role)),
            team -> teamMembershipService.getUserRoles(member, team)
                .forEach(role -> teamMembershipService.removeUserRole(member, team, role)),
            project -> projectMembershipService.getUserRoles(member, project)
                .forEach(role -> projectMembershipService.removeUserRole(member, project, role)),
            OrganizationPermission.EDIT_MEMBERS,
            TeamPermission.EDIT_MEMBERS,
            ProjectPermission.EDIT_MEMBERS
        );
    }

    /**
     * This is the same as
     * {@link #transformEntity(UUID, Function, Function, Function, Permission, Permission, Permission)} except that
     * it supports functions without a return type.
     *
     * @param entityId The ID of the entity to process.
     * @param organizationConsumer The function to apply if the entity is an organization
     * @param teamConsumer The function to apply if the entity is a team
     * @param projectConsumer The function to apply if the entity is a project
     * @param organizationPermission The permission required for the organization entity
     * @param teamPermission The permission required for the team entity
     * @param projectPermission The permission required for the project entity
     * @throws SafaItemNotFoundError If the specified ID did not map to an organization, a team, or a project
     */
    private void consumeEntity(UUID entityId, Consumer<Organization> organizationConsumer,
                               Consumer<Team> teamConsumer, Consumer<Project> projectConsumer,
                               Permission organizationPermission, Permission teamPermission,
                               Permission projectPermission) {
        transformEntity(
            entityId,
            org -> {
                organizationConsumer.accept(org);
                return null;
            },
            team -> {
                teamConsumer.accept(team);
                return null;
            },
            project -> {
                projectConsumer.accept(project);
                return null;
            },
            organizationPermission,
            teamPermission,
            projectPermission
        );
    }

    /**
    * Modify an organization membership by removing the current role and adding a new one
    *
    * @param membershipId The ID of the original membership
    * @param org The organization the membership is in
    * @param newRole The new role to give the user. Set to null to delete the membership
    * @return The new membership
    */
    private OrganizationMembership modifyOrgMembership(UUID membershipId, Organization org, String newRole) {
        OrganizationMembership currentMembership = orgMembershipService.getMembershipById(membershipId);
        SafaUser member = currentMembership.getUser();

        assertEqual(currentMembership.getOrganization().getId(), org.getId(),
            "No membership with the given ID found in the current org");

        orgMembershipService.removeUserRole(member, org, currentMembership.getRole());

        if (newRole != null) {
            return orgMembershipService.addUserRole(member, org, OrganizationRole.valueOf(newRole));
        } else {
            return null;
        }
    }

    /**
     * Modify a team membership by removing the current role and adding a new one
     *
     * @param membershipId The ID of the original membership
     * @param team The team the membership is in
     * @param newRole The new role to give the user. Set to null to delete the membership
     * @return The new membership
     */
    private TeamMembership modifyTeamMembership(UUID membershipId, Team team, String newRole) {
        TeamMembership currentMembership = teamMembershipService.getMembershipById(membershipId);
        SafaUser member = currentMembership.getUser();

        assertEqual(currentMembership.getTeam().getId(), team.getId(),
            "No membership with the given ID found in the current team");

        teamMembershipService.removeUserRole(member, team, currentMembership.getRole());

        if (newRole != null) {
            return teamMembershipService.addUserRole(member, team, TeamRole.valueOf(newRole));
        } else {
            return null;
        }
    }

    /**
     * Modify a project membership by removing the current role and adding a new one
     *
     * @param membershipId The ID of the original membership
     * @param project The project the membership is in
     * @param newRole The new role to give the user. Set to null to delete the membership
     * @return The new membership
     */
    private ProjectMembership modifyProjectMembership(UUID membershipId, Project project, String newRole) {
        ProjectMembership currentMembership = projectMembershipService.getUserMembershipById(membershipId);
        SafaUser member = currentMembership.getMember();

        assertEqual(currentMembership.getProject().getProjectId(), project.getProjectId(),
            "No membership with the given ID found in the current project");

        projectMembershipService.removeUserRole(member, project, currentMembership.getRole());

        if (newRole != null) {
            return projectMembershipService.addUserRole(member, project, ProjectRole.valueOf(newRole));
        } else {
            return null;
        }
    }

    /**
     * Apply a function to the entity specified by the ID and return the result. A different
     * function can be specified for if the entity is an organization, a team, or a project,
     * but all functions must return the same time (or types which are implicitly convertible
     * to the same type)
     *
     * @param entityId The ID of the entity to process.
     * @param organizationFunction The function to apply if the entity is an organization
     * @param teamFunction The function to apply if the entity is a team
     * @param projectFunction The function to apply if the entity is a project
     * @param organizationPermission The permission required for the organization entity
     * @param teamPermission The permission required for the team entity
     * @param projectPermission The permission required for the project entity
     * @param <T> The return type of the functions
     * @return The result of whichever function gets called
     * @throws SafaItemNotFoundError If the specified ID did not map to an organization, a team, or a project
     */
    private <T> T transformEntity(UUID entityId, Function<Organization, T> organizationFunction,
                                  Function<Team, T> teamFunction, Function<Project, T> projectFunction,
                                  Permission organizationPermission, Permission teamPermission,
                                  Permission projectPermission) {
        Optional<Organization> optionalOrganization = organizationService.getOrganizationOptionalById(entityId);
        if (optionalOrganization.isPresent()) {
            permissionService.requirePermission(organizationPermission, optionalOrganization.get(), getCurrentUser());
            return organizationFunction.apply(optionalOrganization.get());
        }

        Optional<Team> optionalTeam = teamService.getTeamOptionalById(entityId);
        if (optionalTeam.isPresent()) {
            permissionService.requirePermission(teamPermission, optionalTeam.get(), getCurrentUser());
            return teamFunction.apply(optionalTeam.get());
        }

        Optional<Project> optionalProject = projectService.getProjectOptionalById(entityId);
        if (optionalProject.isPresent()) {
            permissionService.requirePermission(projectPermission, optionalProject.get(), getCurrentUser());
            return projectFunction.apply(optionalProject.get());
        }

        throw createNoEntityFoundError();
    }

    /**
     * Common function to create an exception for when an ID did not map to a supported entity
     *
     * @return The exception
     */
    private SafaItemNotFoundError createNoEntityFoundError() {
        return new SafaItemNotFoundError("No entity with the given ID found.");
    }

    /**
     * Convert a list of entity memberships into {@link MembershipAppEntity} objects
     *
     * @param memberships The entities to convert
     * @return The converted entities
     */
    private List<MembershipAppEntity> toAppEntities(List<? extends EntityMembership> memberships) {
        return memberships.stream().map(MembershipAppEntity::new).collect(Collectors.toUnmodifiableList());
    }
}
