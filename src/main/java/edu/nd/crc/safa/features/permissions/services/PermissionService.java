package edu.nd.crc.safa.features.permissions.services;

import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.function.BiFunction;
import java.util.function.Function;

import edu.nd.crc.safa.features.memberships.services.OrganizationMembershipService;
import edu.nd.crc.safa.features.memberships.services.ProjectMembershipService;
import edu.nd.crc.safa.features.memberships.services.TeamMembershipService;
import edu.nd.crc.safa.features.organizations.entities.db.IEntityWithMembership;
import edu.nd.crc.safa.features.organizations.entities.db.IRole;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.permissions.MissingPermissionException;
import edu.nd.crc.safa.features.permissions.entities.Permission;
import edu.nd.crc.safa.features.permissions.entities.SafaApplicationPermission;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.AllArgsConstructor;
import lombok.Data;
import org.springframework.context.annotation.Lazy;
import org.springframework.stereotype.Service;

@Service
public class PermissionService {

    private final Map<Class<? extends IEntityWithMembership>, ConfigForType> configForTypeMap;

    public PermissionService(@Lazy OrganizationMembershipService orgMembershipService,
                             @Lazy ProjectMembershipService projectMembershipService,
                             @Lazy TeamMembershipService teamMembershipService) {
        configForTypeMap = Map.of(
            Organization.class, new ConfigForType(orgMembershipService::getRolesForUser,
                entity -> null),
            Team.class, new ConfigForType(teamMembershipService::getRolesForUser,
                entity -> ((Team) entity).getOrganization()),
            Project.class, new ConfigForType(projectMembershipService::getRolesForUser,
                entity -> ((Project) entity).getOwningTeam())
        );
    }

    /**
     * Returns whether the user has the given permission within the given entity.
     *
     * @param permission The permission to check
     * @param entity The entity we're considering
     * @param user The user in question
     * @return Whether the user has the given permission
     */
    public boolean hasPermission(Permission permission, IEntityWithMembership entity, SafaUser user) {
        return checkPermission(permission, getUserPermissions(user, entity), user);
    }

    /**
     * Returns whether the user has the given permissions within the given entity.
     *
     * @param permissions The permissions to check
     * @param entity The entity we're considering
     * @param user The user in question
     * @return Whether the user has the given permissions
     */
    public boolean hasPermissions(Set<Permission> permissions, IEntityWithMembership entity, SafaUser user) {
        return checkPermissionsAllMatch(permissions, getUserPermissions(user, entity), user);
    }

    /**
     * Returns whether the user has any of the given permissions within the given entity.
     *
     * @param permissions The permissions to check
     * @param entity The entity we're considering
     * @param user The user in question
     * @return Whether the user has any of the given permissions
     */
    public boolean hasAnyPermission(Set<Permission> permissions, IEntityWithMembership entity, SafaUser user) {
        return checkPermissionsAnyMatch(permissions, getUserPermissions(user, entity), user);
    }

    /**
     * Returns whether the given user is a superuser and their superuser powers are active.
     *
     * @param user The user in question
     * @return Whether the user is an active superuser
     */
    public boolean isActiveSuperuser(SafaUser user) {
        return isSuperuser(user) && user.isSuperuserActive();
    }

    /**
     * Returns whether the given user is a superuser
     *
     * @param user The user in question
     * @return Whether the user is a superuser
     */
    public boolean isSuperuser(SafaUser user) {
        return user.isSuperuser();
    }

    /**
     * Throws an exception if the user does not have the given permission within the given entity.
     *
     * @param permission The permission to check
     * @param entity The entity we're considering
     * @param user The user in question
     */
    public void requirePermission(Permission permission, IEntityWithMembership entity, SafaUser user) {
        if (!hasPermission(permission, entity, user)) {
            throw new MissingPermissionException(permission);
        }
    }

    /**
     * Throws an exception if the user does not have the given permissions within the given entity.
     *
     * @param permissions The permissions to check
     * @param entity The entity we're considering
     * @param user The user in question
     */
    public void requirePermissions(Set<Permission> permissions, IEntityWithMembership entity, SafaUser user) {
        if (!hasPermissions(permissions, entity, user)) {
            throw new MissingPermissionException(permissions, true);
        }
    }

    /**
     * Throws an exception if the user does not have any of the given permissions within the given entity.
     *
     * @param permissions The permissions to check
     * @param entity The entity we're considering
     * @param user The user in question
     */
    public void requireAnyPermission(Set<Permission> permissions, IEntityWithMembership entity, SafaUser user) {
        if (!hasAnyPermission(permissions, entity, user)) {
            throw new MissingPermissionException(permissions, false);
        }
    }

    /**
     * Throws an exception if the given user is not a superuser.
     *
     * @param user The user in question
     */
    public void requireActiveSuperuser(SafaUser user) {
        requireSuperuser(user);

        if (!isActiveSuperuser(user)) {
            throw new MissingPermissionException(SafaApplicationPermission.SUPERUSER_ACTIVATION);
        }
    }

    /**
     * Throws an exception if the given user is not a superuser.
     *
     * @param user The user in question
     */
    public void requireSuperuser(SafaUser user) {
        if (!isSuperuser(user)) {
            throw new MissingPermissionException(SafaApplicationPermission.SUPERUSER);
        }
    }

    /**
     * Get the next highest entity in the permission hierarchy. <br>
     * <br>
     * Project -> Team -> Organization -> null
     *
     * @param entity The current entity
     * @return The next entity up in the hierarchy
     */
    private IEntityWithMembership getNextEntity(IEntityWithMembership entity) {
        if (configForTypeMap.containsKey(entity.getClass())) {
            return configForTypeMap.get(entity.getClass()).getNextEntityFunction().apply(entity);
        } else {
            throw new IllegalArgumentException("Unknown entity: " + entity.getClass());
        }
    }

    /**
     * Get the set of permissions the given user has associated with the given entity.
     * This function will call the appropriate overload for the entity's type.
     *
     * @param user The user in question
     * @param entity The entity we're considering
     * @return The set of permissions the user has for that entity
     */
    public Set<Permission> getUserPermissions(SafaUser user, IEntityWithMembership entity) {
        Set<Permission> permissions = new HashSet<>();

        while (entity != null) {
            List<IRole> roles = getUserRoles(user, entity);
            roles.forEach(role -> permissions.addAll(role.getGrants()));
            entity = getNextEntity(entity);
        }

        return permissions;
    }

    /**
     * Gets the list of roles a user has associated with a given entity.
     *
     * @param user The user in question
     * @param entity The entity we're considering
     * @return The list of roles the user has associated with that entity
     */
    public List<IRole> getUserRoles(SafaUser user, IEntityWithMembership entity) {
        if (configForTypeMap.containsKey(entity.getClass())) {
            return configForTypeMap.get(entity.getClass()).getRoleRetrievalFunction().apply(user, entity);
        } else {
            throw new IllegalArgumentException("Unknown entity: " + entity.getClass());
        }
    }

    /**
     * Checks that all required permissions are in the user permission set.
     *
     * @param requiredPermissions All permissions that are required
     * @param userPermissions All permissions that the user has
     * @param user The user to check. If the user is a superuser, the function always returns true
     * @return Whether the user has all required permissions
     */
    private boolean checkPermissionsAllMatch(Set<Permission> requiredPermissions, Set<Permission> userPermissions,
                                             SafaUser user) {
        if (isActiveSuperuser(user)) {
            return true;
        }
        return userPermissions.containsAll(requiredPermissions);
    }

    /**
     * Checks that any required permission is in the user permission set.
     *
     * @param requiredPermissions Set of permissions to check
     * @param userPermissions All permissions that the user has
     * @param user The user to check. If the user is a superuser, the function always returns true
     * @return Whether the user has any of the required permissions
     */
    private boolean checkPermissionsAnyMatch(Set<Permission> requiredPermissions, Set<Permission> userPermissions,
                                             SafaUser user) {
        if (isActiveSuperuser(user)) {
            return true;
        }
        return requiredPermissions.stream().anyMatch(userPermissions::contains);
    }

    /**
     * Checks that the required permissions is in the user permission set.
     *
     * @param requiredPermission The required permission
     * @param userPermissions All permissions that the user has
     * @param user The user to check. If the user is a superuser, the function always returns true
     * @return Whether the user has the required permission
     */
    private boolean checkPermission(Permission requiredPermission, Set<Permission> userPermissions, SafaUser user) {
        if (isActiveSuperuser(user)) {
            return true;
        }
        return userPermissions.contains(requiredPermission);
    }

    /**
     * A configuration object that holds all of the things we need to associate
     * with a given entity type
     */
    @Data
    @AllArgsConstructor
    private static class ConfigForType {
        private BiFunction<SafaUser, IEntityWithMembership, List<IRole>> roleRetrievalFunction;
        private Function<IEntityWithMembership, IEntityWithMembership> nextEntityFunction;
    }
}
