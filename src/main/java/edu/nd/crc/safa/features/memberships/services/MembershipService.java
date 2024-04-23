package edu.nd.crc.safa.features.memberships.services;

import static edu.nd.crc.safa.utilities.AssertUtils.assertEqual;

import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.UUID;
import java.util.function.Function;

import edu.nd.crc.safa.features.memberships.entities.db.IEntityMembership;
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
import edu.nd.crc.safa.features.projects.entities.app.SafaItemNotFoundError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.services.ProjectService;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.AllArgsConstructor;
import lombok.Data;
import org.springframework.stereotype.Service;

/**
 * Responsible for CRUD operations related to project memberships
 */
@Service
public class MembershipService {

    private final OrganizationService organizationService;
    private final ProjectService projectService;
    private final TeamService teamService;

    private final TeamMembershipService teamMembershipService;
    private final OrganizationMembershipService orgMembershipService;
    private final ProjectMembershipService projectMembershipService;

    private final PermissionService permissionService;

    private final Map<Class<? extends IEntityWithMembership>, ConfigForType> entityTypeConfigMap;

    public MembershipService(OrganizationService organizationService, ProjectService projectService,
                             TeamService teamService, TeamMembershipService teamMembershipService,
                             OrganizationMembershipService orgMembershipService,
                             ProjectMembershipService projectMembershipService, PermissionService permissionService) {
        this.organizationService = organizationService;
        this.projectService = projectService;
        this.teamService = teamService;
        this.teamMembershipService = teamMembershipService;
        this.orgMembershipService = orgMembershipService;
        this.projectMembershipService = projectMembershipService;
        this.permissionService = permissionService;

        this.entityTypeConfigMap = Map.of(
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
     * Get a list of memberships for a particular project. As opposed to {@link #getMembers(UUID, SafaUser)}, this
     * function combines all team and project memberships together into a single list
     *
     * @param project The project
     * @param requester The user making the request (to check permissions)
     * @return The list of memberships representing all users who have access to this project
     */
    public List<MembershipAppEntity> getMembershipsInProject(Project project, SafaUser requester) {
        permissionService.requirePermission(getViewPermission(project), project, requester);
        List<MembershipAppEntity> projectMembers = teamMembershipService.getProjectMemberships(project);
        List<MembershipAppEntity> invitedMembers = projectMembershipService.getProjectMemberships(project);
        projectMembers.addAll(invitedMembers);
        return projectMembers;
    }

    /**
     * Get a list of memberships for the given entity. Unlike {@link #getMembershipsInProject(Project, SafaUser)}, if
     * this function is given a project, it will only return the list of direct project memberships, without accounting
     * for any team memberships that may give a user access to the project
     *
     * @param entityId The ID of the entity
     * @param asUser The user making the request (to check permissions)
     * @return The list of memberships in this entity
     */
    public List<IEntityMembership> getMembers(UUID entityId, SafaUser asUser) {
        IEntityWithMembership entity = getEntity(entityId);
        permissionService.requirePermission(getViewPermission(entity), entity, asUser);
        IMembershipService membershipService = getSpecificMembershipService(entity);
        return membershipService.getMembershipsForEntity(entity);
    }

    public List<MembershipAppEntity> getAppEntitiesByIds(Project project, SafaUser user, List<UUID> appEntityIds) {
        Set<UUID> uuidSet = new HashSet<>(appEntityIds);
        return getMembershipsInProject(project, user)
                .stream()
                .filter(m -> uuidSet.contains(m.getId()))
                .toList();
    }

    /**
     * Create a new membership within a given entity. This function will check the permissions of {@code asUser}
     * to ensure that they are allowed to create the membership
     *
     * @param entityId The membership will be created within the entity with this ID
     * @param roleName The name of the role to give the user
     * @param forUser The user receiving the new membership
     * @param asUser The user creating the new membership (to check permissions)
     * @return The new membership
     */
    public IEntityMembership createMembership(UUID entityId, String roleName, SafaUser forUser, SafaUser asUser) {
        IEntityWithMembership entity = getEntity(entityId);
        permissionService.requirePermission(getEditMembersPermission(entity), entity, asUser);
        IRole role = getRoleForEntity(entity, roleName);
        return createMembership(forUser, entity, role);
    }

    /**
     * Create a new membership. Unlike {@link #createMembership(UUID, String, SafaUser, SafaUser)}, this
     * function does not do any permission checking
     *
     * @param member The member to create a membership for
     * @param entity The entity to create the membership within
     * @param role The role to give the user
     * @return The new membership
     */
    public IEntityMembership createMembership(SafaUser member, IEntityWithMembership entity, IRole role) {
        IMembershipService membershipService = getSpecificMembershipService(entity);
        return membershipService.addUserRole(member, entity, role);
    }

    /**
     * Convenience function to update the role of a user. This function will first delete the original
     * membership and then create a new one with the new role, so the returned membership will not have
     * the same ID as the one supplied
     *
     * @param entityId The membership will be created within this entity
     * @param membershipId The ID of the membership to update (remove)
     * @param roleName The new role to give the user
     * @param asUser The user making the request (to check permissions)
     * @return The updated (new) membership
     */
    public IEntityMembership updateMembership(UUID entityId, UUID membershipId, String roleName, SafaUser asUser) {
        IEntityWithMembership entity = getEntity(entityId);
        permissionService.requirePermission(getEditMembersPermission(entity), entity, asUser);
        IRole role = getRoleForEntity(entity, roleName);
        IMembershipService membershipService = getSpecificMembershipService(entity);
        IEntityMembership currentMembership = membershipService.getMembershipById(membershipId);
        SafaUser editedUser = deleteMembership(currentMembership, entity);
        return createMembership(editedUser, entity, role);
    }

    /**
     * Delete a membership
     *
     * @param entityId The membership to delete must exist within the entity with this ID
     * @param membershipId The ID of the membership
     * @param asUser The user making the request (to check permissions)
     */
    public void deleteMembership(UUID entityId, UUID membershipId, SafaUser asUser) {
        IEntityWithMembership entity = getEntity(entityId);
        IMembershipService membershipService = getSpecificMembershipService(entity);
        IEntityMembership currentMembership = membershipService.getMembershipById(membershipId);
        SafaUser modifiedUser = currentMembership.getUser();

        if (!asUser.equals(modifiedUser)) {
            permissionService.requirePermission(getEditMembersPermission(entity), entity, asUser);
        }
        deleteMembership(currentMembership, entity);
    }

    /**
     * Delete the membership in the given entity and return the user that it represented.
     *
     * @param currentMembership The membership
     * @param entity The entity the membership exists within (this will be checked and an exception is
     *               thrown if the membership with the given ID doesn't exist within the given entity)
     * @return The user that had the membership, so that further operations can be performed on them if needed
     */
    public SafaUser deleteMembership(IEntityMembership currentMembership, IEntityWithMembership entity) {
        IMembershipService membershipService = getSpecificMembershipService(entity);
        SafaUser member = currentMembership.getUser();

        assertEqual(currentMembership.getEntity().getId(), entity.getId(),
                "No membership with the given ID found");

        membershipService.removeUserRole(member, entity, currentMembership.getRole());
        return currentMembership.getUser();
    }

    /**
     * Delete all memberships within a given entity for a given user
     *
     * @param entityId The entity
     * @param forUser The user to update
     * @param asUser The user making the request (to check permissions)
     */
    public void deleteAllUserMemberships(UUID entityId, SafaUser forUser, SafaUser asUser) {
        IEntityWithMembership entity = getEntity(entityId);

        if (!asUser.equals(forUser)) {
            permissionService.requirePermission(getEditMembersPermission(entity), entity, asUser);
        }

        IMembershipService membershipService = getSpecificMembershipService(entity);
        List<IRole> roles = membershipService.getRolesForUser(forUser, entity);
        roles.forEach(role -> membershipService.removeUserRole(forUser, entity, role));
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
     * Get a role with the given name which has the appropriate type for memberships within
     * the given entity.
     *
     * @param entity The entity which would (potentially) contain memberships with the given role
     * @param role The name of the role to look up
     * @return The role
     */
    public IRole getRoleForEntity(IEntityWithMembership entity, String role) {
        return getTypeConfigForEntity(entity).getRoleParseFunction().apply(role);
    }

    /**
     * Get the membership service which handles memberships for the given entity
     *
     * @param entity The entity
     * @return The service to use to handle that entity's memberships
     */
    private IMembershipService getSpecificMembershipService(IEntityWithMembership entity) {
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
     * Retrieve the entity with the given ID, regardless of its type
     *
     * @param entityId The ID of the entity to get
     * @return The entity with that ID, as long as it is one of the recognized types and it exists
     */
    public IEntityWithMembership getEntity(UUID entityId) {
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
     * Common function to create an exception for when an ID did not map to a supported entity
     *
     * @return The exception
     */
    private SafaItemNotFoundError createNoEntityFoundError() {
        return new SafaItemNotFoundError("No entity with the given ID found.");
    }

    @Data
    @AllArgsConstructor
    private static class ConfigForType {
        private IMembershipService membershipService;
        private Permission viewPermission;
        private Permission editMembersPermission;
        private Function<String, IRole> roleParseFunction;
    }
}
