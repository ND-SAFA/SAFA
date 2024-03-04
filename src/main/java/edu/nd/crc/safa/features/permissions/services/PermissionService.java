package edu.nd.crc.safa.features.permissions.services;

import java.time.Duration;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;
import java.util.function.BiFunction;
import java.util.function.Function;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.memberships.services.OrganizationMembershipService;
import edu.nd.crc.safa.features.memberships.services.ProjectMembershipService;
import edu.nd.crc.safa.features.memberships.services.TeamMembershipService;
import edu.nd.crc.safa.features.organizations.entities.db.IEntityWithMembership;
import edu.nd.crc.safa.features.organizations.entities.db.IRole;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.permissions.MissingPermissionException;
import edu.nd.crc.safa.features.permissions.checks.AdditionalPermissionCheck;
import edu.nd.crc.safa.features.permissions.checks.PermissionCheckContext;
import edu.nd.crc.safa.features.permissions.checks.utility.AndPermissionCheck;
import edu.nd.crc.safa.features.permissions.checks.utility.OrPermissionCheck;
import edu.nd.crc.safa.features.permissions.entities.Permission;
import edu.nd.crc.safa.features.permissions.entities.SafaApplicationPermission;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.utilities.ExpiringValue;

import lombok.AllArgsConstructor;
import lombok.Data;
import org.springframework.context.annotation.Lazy;
import org.springframework.stereotype.Service;

@Service
public class PermissionService {

    private final Map<Class<? extends IEntityWithMembership>, ConfigForType> configForTypeMap;
    private final Map<UUID, ExpiringValue<Boolean>> isSuperuserActiveMap;
    private final ServiceProvider serviceProvider;

    public PermissionService(@Lazy OrganizationMembershipService orgMembershipService,
                             @Lazy ProjectMembershipService projectMembershipService,
                             @Lazy TeamMembershipService teamMembershipService,
                             @Lazy ServiceProvider serviceProvider) {
        configForTypeMap = Map.of(
            Organization.class, new ConfigForType(orgMembershipService::getRolesForUser,
                entity -> null),
            Team.class, new ConfigForType(teamMembershipService::getRolesForUser,
                entity -> ((Team) entity).getOrganization()),
            Project.class, new ConfigForType(projectMembershipService::getRolesForUser,
                entity -> ((Project) entity).getOwningTeam()),
            ProjectVersion.class, new ConfigForType((user, entity) -> new ArrayList<>(),
                entity -> ((ProjectVersion) entity).getProject())
        );
        this.isSuperuserActiveMap = new HashMap<>();
        this.serviceProvider = serviceProvider;
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
        PermissionCheckContext context = createContext(entity, user);
        Set<Permission> userPermissions = getUserPermissions(user, entity);
        return checkPermission(permission, userPermissions, user, context);
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
        PermissionCheckContext context = createContext(entity, user);
        Set<Permission> userPermissions = getUserPermissions(user, entity);
        return checkPermissionsAllMatch(permissions, userPermissions, user, context);
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
        PermissionCheckContext context = createContext(entity, user);
        Set<Permission> userPermissions = getUserPermissions(user, entity);
        return checkPermissionsAnyMatch(permissions, userPermissions, user, context);
    }

    /**
     * Checks if an {@link AdditionalPermissionCheck} passes for the given user in the given entity.
     *
     * @param check The additional permission check to perform. These can be chained together using
     *              {@link AndPermissionCheck} and {@link OrPermissionCheck}
     * @param entity The entity we're considering
     * @param user The user in question
     * @return Whether the check passes for that user
     */
    public boolean hasAdditionalCheck(AdditionalPermissionCheck check, IEntityWithMembership entity, SafaUser user) {
        PermissionCheckContext context = createContext(entity, user);
        return doAdditionalCheck(context, check, user);
    }

    /**
     * Checks if an {@link AdditionalPermissionCheck} passes for the given user.
     *
     * @param check The additional permission check to perform. These can be chained together using
     *              {@link AndPermissionCheck} and {@link OrPermissionCheck}
     * @param user The user in question
     * @return Whether the check passes for that user
     */
    public boolean hasAdditionalCheck(AdditionalPermissionCheck check, SafaUser user) {
        PermissionCheckContext context = createContext(user);
        return doAdditionalCheck(context, check, user);
    }

    /**
     * Actually do a check
     *
     * @param context The check context
     * @param check The check
     * @param user The user trying to perform an action
     * @return Whether the check passes for that user
     */
    private boolean doAdditionalCheck(PermissionCheckContext context, AdditionalPermissionCheck check, SafaUser user) {
        if (check.superuserCanOverride() && isActiveSuperuser(user)) {
            return true;
        }
        return check.doCheck(context);
    }

    /**
     * Create a permission check context object for a given entity
     *
     * @param entity The entity to put in the context
     * @param user The user to put in the context
     * @return The constructed context
     */
    private PermissionCheckContext createContext(IEntityWithMembership entity, SafaUser user) {
        return PermissionCheckContext.builder()
            .add(user)
            .add(entity)
            .add(serviceProvider)
            .get();
    }

    /**
     * Create a permission check context object without an entity
     *
     * @param user The user to put in the context
     * @return The constructed context
     */
    private PermissionCheckContext createContext(SafaUser user) {
        return PermissionCheckContext.builder()
            .add(user)
            .add(serviceProvider)
            .get();
    }

    /**
     * Returns whether the given user is a superuser and their superuser powers are active.
     *
     * @param user The user in question
     * @return Whether the user is an active superuser
     */
    public boolean isActiveSuperuser(SafaUser user) {
        return isSuperuser(user) && getSuperuserActiveValue(user).getAndRefresh();
    }

    /**
     * Set whether the current user's superuser powers are active. This will throw an exception if the
     * user is not a superuser. Superuser activation is automatically disabled after 1 hour without being used.
     *
     * @param user The user to act on
     * @param active Whether the user's superuser powers should be active
     */
    public void setActiveSuperuser(SafaUser user, boolean active) {
        if (active && !user.isSuperuser()) {
            throw new SafaError("Setting superuser activation on user who is not superuser - " + user.getEmail());
        }
        ExpiringValue<Boolean> superuserActive = getSuperuserActiveValue(user);
        superuserActive.set(active);
    }

    /**
     * Get the current superuser activity value for the given user, or create it if it doesn't exist
     *
     * @param user The user
     * @return The user's superuser activity status
     */
    private ExpiringValue<Boolean> getSuperuserActiveValue(SafaUser user) {
        if (!isSuperuserActiveMap.containsKey(user.getUserId())) {
            isSuperuserActiveMap.put(user.getUserId(), new ExpiringValue<>(false, Duration.ofHours(1)));
        }
        return isSuperuserActiveMap.get(user.getUserId());
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
     * Throws an exception if the check does not pass for the given user in the given entity.
     *
     * @param check The additional permission check to perform. These can be chained together using
     *              {@link AndPermissionCheck} and {@link OrPermissionCheck}
     * @param entity The entity we're considering
     * @param user The user in question
     */
    public void requireAdditionalCheck(AdditionalPermissionCheck check, IEntityWithMembership entity, SafaUser user) {
        if (!hasAdditionalCheck(check, entity, user)) {
            throw new MissingPermissionException(List.of(check.getMessage()));
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
     * @param context The permission check context so that we can do additional checks on the permission
     * @return Whether the user has all required permissions
     */
    private boolean checkPermissionsAllMatch(Set<Permission> requiredPermissions, Set<Permission> userPermissions,
                                             SafaUser user, PermissionCheckContext context) {
        if (isActiveSuperuser(user)) {
            return true;
        }
        return requiredPermissions.stream().allMatch(perm -> checkPermission(perm, userPermissions, user, context));
    }

    /**
     * Checks that any required permission is in the user permission set.
     *
     * @param requiredPermissions Set of permissions to check
     * @param userPermissions All permissions that the user has
     * @param user The user to check. If the user is a superuser, the function always returns true
     * @param context The permission check context so that we can do additional checks on the permission
     * @return Whether the user has any of the required permissions
     */
    private boolean checkPermissionsAnyMatch(Set<Permission> requiredPermissions, Set<Permission> userPermissions,
                                             SafaUser user, PermissionCheckContext context) {
        if (isActiveSuperuser(user)) {
            return true;
        }
        return requiredPermissions.stream().anyMatch(perm -> checkPermission(perm, userPermissions, user, context));
    }

    /**
     * Checks that the required permissions is in the user permission set.
     *
     * @param requiredPermission The required permission
     * @param userPermissions All permissions that the user has
     * @param user The user to check. If the user is a superuser, the function always returns true
     * @param context The permission check context so that we can do additional checks on the permission
     * @return Whether the user has the required permission
     */
    private boolean checkPermission(Permission requiredPermission, Set<Permission> userPermissions,
                                    SafaUser user, PermissionCheckContext context) {
        if (isActiveSuperuser(user)) {
            return true;
        }

        if (!userPermissions.contains(requiredPermission)) {
            return false;
        }

        return requiredPermission.getAdditionalCheck().doCheck(context);
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
