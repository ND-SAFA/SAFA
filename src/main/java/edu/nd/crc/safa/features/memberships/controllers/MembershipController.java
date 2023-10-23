package edu.nd.crc.safa.features.memberships.controllers;

import static edu.nd.crc.safa.utilities.AssertUtils.assertEqual;

import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;
import java.util.function.Function;
import java.util.stream.Collectors;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.memberships.entities.db.IEntityMembership;
import edu.nd.crc.safa.features.memberships.services.IMembershipService;
import edu.nd.crc.safa.features.memberships.services.OrganizationMembershipService;
import edu.nd.crc.safa.features.memberships.services.ProjectMembershipService;
import edu.nd.crc.safa.features.memberships.services.TeamMembershipService;
import edu.nd.crc.safa.features.organizations.entities.app.MembershipAppEntity;
import edu.nd.crc.safa.features.organizations.entities.db.IEntityWithMembership;
import edu.nd.crc.safa.features.organizations.entities.db.IRole;
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

import lombok.AllArgsConstructor;
import lombok.Data;
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

    private final PermissionService permissionService;

    private final Map<Class<? extends IEntityWithMembership>, ConfigForType> entityTypeConfigMap;

    public MembershipController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider,
                                OrganizationService organizationService, ProjectService projectService,
                                TeamService teamService, OrganizationMembershipService orgMembershipService,
                                ProjectMembershipService projectMembershipService,
                                TeamMembershipService teamMembershipService, PermissionService permissionService) {
        super(resourceBuilder, serviceProvider);
        this.organizationService = organizationService;
        this.projectService = projectService;
        this.teamService = teamService;
        this.permissionService = permissionService;

        entityTypeConfigMap = Map.of(
            Organization.class, new ConfigForType(
                orgMembershipService, OrganizationPermission.VIEW, OrganizationPermission.EDIT_MEMBERS,
                OrganizationRole::valueOf
            ),
            Team.class, new ConfigForType(
                teamMembershipService, TeamPermission.VIEW, TeamPermission.EDIT_MEMBERS, TeamRole::valueOf
            ),
            Project.class, new ConfigForType(
                projectMembershipService, ProjectPermission.VIEW, ProjectPermission.EDIT_MEMBERS, ProjectRole::valueOf
            )
        );
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
        IEntityWithMembership entity = getEntity(entityId);
        permissionService.requirePermission(getViewPermission(entity), entity, getCurrentUser());
        IMembershipService membershipService = getMembershipService(entity);
        List<IEntityMembership> memberships = membershipService.getMembershipsForEntity(entity);
        return toAppEntities(memberships);
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
        IEntityWithMembership entity = getEntity(entityId);
        permissionService.requirePermission(getEditMembersPermission(entity), entity, getCurrentUser());
        IRole role = getRole(entity, newMembership.getRole());
        return new MembershipAppEntity(createMembership(newMember, entity, role));
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
        IEntityWithMembership entity = getEntity(entityId);
        permissionService.requirePermission(getEditMembersPermission(entity), entity, getCurrentUser());
        IRole role = getRole(entity, membership.getRole());
        IMembershipService membershipService = getMembershipService(entity);
        IEntityMembership currentMembership = membershipService.getMembershipById(membershipId);
        SafaUser editedUser = removeMembership(currentMembership, entity);
        return new MembershipAppEntity(createMembership(editedUser, entity, role));
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
        IEntityWithMembership entity = getEntity(entityId);
        IMembershipService membershipService = getMembershipService(entity);
        IEntityMembership currentMembership = membershipService.getMembershipById(membershipId);
        SafaUser currentUser = getCurrentUser();
        SafaUser modifiedUser = currentMembership.getUser();

        if (!currentUser.equals(modifiedUser)) {
            permissionService.requirePermission(getEditMembersPermission(entity), entity, getCurrentUser());
        }
        removeMembership(currentMembership, entity);
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

        IEntityWithMembership entity = getEntity(entityId);
        permissionService.requirePermission(getEditMembersPermission(entity), entity, getCurrentUser());
        IMembershipService membershipService = getMembershipService(entity);
        List<IRole> roles = membershipService.getRolesForUser(member, entity);
        roles.forEach(role -> membershipService.removeUserRole(member, entity, role));
    }

    /**
     * Retrieve the entity with the given ID, regardless of its type
     *
     * @param entityId The ID of the entity to get
     * @return The entity with that ID, as long as it is one of the recognized types and it exists
     */
    private IEntityWithMembership getEntity(UUID entityId) {
        Optional<Organization> optionalOrganization = organizationService.getOrganizationOptionalById(entityId);
        if (optionalOrganization.isPresent()) {
            return optionalOrganization.get();
        }

        Optional<Team> optionalTeam = teamService.getTeamOptionalById(entityId);
        if (optionalTeam.isPresent()) {
            return optionalTeam.get();
        }

        Optional<Project> optionalProject = projectService.getProjectOptionalById(entityId);
        if (optionalProject.isPresent()) {
            return optionalProject.get();
        }

        throw createNoEntityFoundError();
    }

    /**
     * Delete the membership in the given entity and return the user that it represented.
     *
     * @param currentMembership The membership
     * @param entity The entity the membership exists within (this will be checked and an exception is
     *               thrown if the membership with the given ID doesn't exist within the given entity)
     * @return The user that had the membership, so that further operations can be performed on them if needed
     */
    private SafaUser removeMembership(IEntityMembership currentMembership, IEntityWithMembership entity) {
        IMembershipService membershipService = getMembershipService(entity);
        SafaUser member = currentMembership.getUser();

        assertEqual(currentMembership.getEntity().getId(), entity.getId(),
            "No membership with the given ID found");

        membershipService.removeUserRole(member, entity, currentMembership.getRole());
        return currentMembership.getUser();
    }

    /**
     * Create a new membership
     *
     * @param member The member to create a membership for
     * @param entity The entity to create the membership within
     * @param role The role to give the user
     * @return The new membership
     */
    private IEntityMembership createMembership(SafaUser member, IEntityWithMembership entity, IRole role) {
        IMembershipService membershipService = getMembershipService(entity);
        return membershipService.addUserRole(member, entity, role);
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
    private List<MembershipAppEntity> toAppEntities(List<? extends IEntityMembership> memberships) {
        return memberships.stream().map(MembershipAppEntity::new).collect(Collectors.toUnmodifiableList());
    }

    /**
     * Get a role with the given name which has the appropriate type for memberships within
     * the given entity.
     *
     * @param entity The entity which would (potentially) contain memberships with the given role
     * @param role The name of the role to look up
     * @return The role
     */
    private IRole getRole(IEntityWithMembership entity, String role) {
        return getTypeConfigForEntity(entity).getRoleParseFunction().apply(role);
    }

    /**
     * Get the membership service which handles memberships for the given entity
     *
     * @param entity The entity
     * @return The service to use to handle that entity's memberships
     */
    private IMembershipService getMembershipService(IEntityWithMembership entity) {
        return getTypeConfigForEntity(entity).getMembershipService();
    }

    /**
     * Get the permission which decides if a user can view the given entity
     *
     * @param entity The entity
     * @return The permission that says a user can view the entity
     */
    private Permission getViewPermission(IEntityWithMembership entity) {
        return getTypeConfigForEntity(entity).getViewPermission();
    }

    /**
     * Get the permission which decides if a user can edit members within the given entity
     *
     * @param entity The entity
     * @return The permission that says a user can edit members
     */
    private Permission getEditMembersPermission(IEntityWithMembership entity) {
        return getTypeConfigForEntity(entity).getEditMembersPermission();
    }

    /**
     * Get the type config object for a given entity based on its type
     *
     * @param entity The entity
     * @return The config for that entity
     */
    private ConfigForType getTypeConfigForEntity(IEntityWithMembership entity) {
        if (entityTypeConfigMap.containsKey(entity.getClass())) {
            return entityTypeConfigMap.get(entity.getClass());
        }
        throw new IllegalArgumentException("Unknown entity: " + entity.getClass());
    }

    /**
     * A configuration object that holds all of the things we need to associate
     * with a given entity type
     */
    @Data
    @AllArgsConstructor
    private static class ConfigForType {
        private IMembershipService membershipService;
        private Permission viewPermission;
        private Permission editMembersPermission;
        private Function<String, IRole> roleParseFunction;
    }
}
