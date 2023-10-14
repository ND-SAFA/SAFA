package edu.nd.crc.safa.features.permissions.services;

import java.util.HashSet;
import java.util.List;
import java.util.Set;

import edu.nd.crc.safa.features.memberships.services.OrganizationMembershipService;
import edu.nd.crc.safa.features.memberships.services.ProjectMembershipService;
import edu.nd.crc.safa.features.memberships.services.TeamMembershipService;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.OrganizationRole;
import edu.nd.crc.safa.features.organizations.entities.db.ProjectRole;
import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.organizations.entities.db.TeamRole;
import edu.nd.crc.safa.features.permissions.MissingPermissionException;
import edu.nd.crc.safa.features.permissions.entities.Permission;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class PermissionService {

    private final OrganizationMembershipService orgMembershipService;
    private final ProjectMembershipService projectMembershipService;
    private final TeamMembershipService teamMembershipService;

    /**
     * Returns whether the user has the given permission within the given project.
     *
     * @param permission The permission to check
     * @param project The project we're considering
     * @param user The user in question
     * @return Whether the user has the given permission
     */
    public boolean hasPermission(Permission permission, Project project, SafaUser user) {
        return hasPermissions(Set.of(permission), project, user);
    }

    /**
     * Returns whether the user has the given permission within the given team.
     *
     * @param permission The permission to check
     * @param team The team we're considering
     * @param user The user in question
     * @return Whether the user has the given permission
     */
    public boolean hasPermission(Permission permission, Team team, SafaUser user) {
        return hasPermissions(Set.of(permission), team, user);
    }

    /**
     * Returns whether the user has the given permission within the given organization.
     *
     * @param permission The permission to check
     * @param organization The organization we're considering
     * @param user The user in question
     * @return Whether the user has the given permission
     */
    public boolean hasPermission(Permission permission, Organization organization, SafaUser user) {
        return hasPermissions(Set.of(permission), organization, user);
    }

    /**
     * Returns whether the user has the given permissions within the given project.
     *
     * @param permissions The permissions to check
     * @param project The project we're considering
     * @param user The user in question
     * @return Whether the user has the given permissions
     */
    public boolean hasPermissions(Set<Permission> permissions, Project project, SafaUser user) {
        if (user.isSuperuser()) {
            return true;
        }

        return getUserPermissions(user, project).containsAll(permissions);
    }

    /**
     * Returns whether the user has the given permissions within the given team.
     *
     * @param permissions The permissions to check
     * @param team The team we're considering
     * @param user The user in question
     * @return Whether the user has the given permissions
     */
    public boolean hasPermissions(Set<Permission> permissions, Team team, SafaUser user) {
        if (user.isSuperuser()) {
            return true;
        }

        return getUserPermissions(user, team).containsAll(permissions);
    }

    /**
     * Returns whether the user has the given permissions within the given organization.
     *
     * @param permissions The permissions to check
     * @param organization The organization we're considering
     * @param user The user in question
     * @return Whether the user has the given permissions
     */
    public boolean hasPermissions(Set<Permission> permissions, Organization organization, SafaUser user) {
        if (user.isSuperuser()) {
            return true;
        }

        return getUserPermissions(user, organization).containsAll(permissions);
    }

    /**
     * Returns whether the user has any of the given permissions within the given project.
     *
     * @param permissions The permissions to check
     * @param project The project we're considering
     * @param user The user in question
     * @return Whether the user has any of the given permissions
     */
    public boolean hasAnyPermission(Set<Permission> permissions, Project project, SafaUser user) {
        if (user.isSuperuser()) {
            return true;
        }

        Set<Permission> userPermissions = getUserPermissions(user, project);
        return permissions.stream().anyMatch(userPermissions::contains);
    }

    /**
     * Returns whether the user has any of the given permissions within the given team.
     *
     * @param permissions The permissions to check
     * @param team The team we're considering
     * @param user The user in question
     * @return Whether the user has any of the given permissions
     */
    public boolean hasAnyPermission(Set<Permission> permissions, Team team, SafaUser user) {
        if (user.isSuperuser()) {
            return true;
        }

        Set<Permission> userPermissions = getUserPermissions(user, team);
        return permissions.stream().anyMatch(userPermissions::contains);
    }

    /**
     * Returns whether the user has any of the given permissions within the given organization.
     *
     * @param permissions The permissions to check
     * @param organization The organization we're considering
     * @param user The user in question
     * @return Whether the user has any of the given permissions
     */
    public boolean hasAnyPermission(Set<Permission> permissions, Organization organization, SafaUser user) {
        if (user.isSuperuser()) {
            return true;
        }

        Set<Permission> userPermissions = getUserPermissions(user, organization);
        return permissions.stream().anyMatch(userPermissions::contains);
    }

    /**
     * Throws an exception if the user does not have the given permission within the given project.
     *
     * @param permission The permission to check
     * @param project The project we're considering
     * @param user The user in question
     */
    public void requirePermission(Permission permission, Project project, SafaUser user) {
        if (!hasPermission(permission, project, user)) {
            throw new MissingPermissionException(permission);
        }
    }

    /**
     * Throws an exception if the user does not have the given permission within the given team.
     *
     * @param permission The permission to check
     * @param team The team we're considering
     * @param user The user in question
     */
    public void requirePermission(Permission permission, Team team, SafaUser user) {
        if (!hasPermission(permission, team, user)) {
            throw new MissingPermissionException(permission);
        }
    }

    /**
     * Throws an exception if the user does not have the given permission within the given organization.
     *
     * @param permission The permission to check
     * @param organization The organization we're considering
     * @param user The user in question
     */
    public void requirePermission(Permission permission, Organization organization, SafaUser user) {
        if (!hasPermission(permission, organization, user)) {
            throw new MissingPermissionException(permission);
        }
    }

    /**
     * Throws an exception if the user does not have the given permissions within the given project.
     *
     * @param permissions The permissions to check
     * @param project The project we're considering
     * @param user The user in question
     */
    public void requirePermissions(Set<Permission> permissions, Project project, SafaUser user) {
        if (!hasPermissions(permissions, project, user)) {
            throw new MissingPermissionException(permissions, true);
        }
    }

    /**
     * Throws an exception if the user does not have the given permissions within the given team.
     *
     * @param permissions The permissions to check
     * @param team The team we're considering
     * @param user The user in question
     */
    public void requirePermissions(Set<Permission> permissions, Team team, SafaUser user) {
        if (!hasPermissions(permissions, team, user)) {
            throw new MissingPermissionException(permissions, true);
        }
    }

    /**
     * Throws an exception if the user does not have the given permissions within the given organization.
     *
     * @param permissions The permissions to check
     * @param organization The organization we're considering
     * @param user The user in question
     */
    public void requirePermissions(Set<Permission> permissions, Organization organization, SafaUser user) {
        if (!hasPermissions(permissions, organization, user)) {
            throw new MissingPermissionException(permissions, true);
        }
    }

    /**
     * Throws an exception if the user does not have any of the given permissions within the given project.
     *
     * @param permissions The permissions to check
     * @param project The project we're considering
     * @param user The user in question
     */
    public void requireAnyPermission(Set<Permission> permissions, Project project, SafaUser user) {
        if (!hasAnyPermission(permissions, project, user)) {
            throw new MissingPermissionException(permissions, false);
        }
    }

    /**
     * Throws an exception if the user does not have any of the given permissions within the given team.
     *
     * @param permissions The permissions to check
     * @param team The team we're considering
     * @param user The user in question
     */
    public void requireAnyPermission(Set<Permission> permissions, Team team, SafaUser user) {
        if (!hasAnyPermission(permissions, team, user)) {
            throw new MissingPermissionException(permissions, false);
        }
    }

    /**
     * Throws an exception if the user does not have any of the given permissions within the given organization.
     *
     * @param permissions The permissions to check
     * @param organization The organization we're considering
     * @param user The user in question
     */
    public void requireAnyPermission(Set<Permission> permissions, Organization organization, SafaUser user) {
        if (!hasAnyPermission(permissions, organization, user)) {
            throw new MissingPermissionException(permissions, false);
        }
    }

    /**
     * Get the set of permissions the given user has associated with the given project.
     * This function will use the project role, team role, and organization role together
     * to determine what actions the user can perform.
     *
     * @param user The user in question
     * @param project The project we're considering
     * @return The set of permissions the user has for that project
     */
    public Set<Permission> getUserPermissions(SafaUser user, Project project) {
        List<ProjectRole> projectRoles = getUserRoles(user, project);

        Set<Permission> permissions = new HashSet<>();
        projectRoles.forEach(role -> permissions.addAll(role.getGrants()));
        permissions.addAll(getUserPermissions(user, project.getOwningTeam()));
        return permissions;
    }

    /**
     * Get the set of permissions the given user has associated with the given team.
     * This function will use the team role and organization role together
     * to determine what actions the user can perform.
     *
     * @param user The user in question
     * @param team The team we're considering
     * @return The set of permissions the user has for that team
     */
    public Set<Permission> getUserPermissions(SafaUser user, Team team) {
        List<TeamRole> teamRoles = getUserRoles(user, team);

        Set<Permission> permissions = new HashSet<>();
        teamRoles.forEach(role -> permissions.addAll(role.getGrants()));
        permissions.addAll(getUserPermissions(user, team.getOrganization()));
        return permissions;
    }

    /**
     * Get the set of permissions the given user has associated with the given organization.
     * This function will use the organization role to determine what actions the user can perform.
     *
     * @param user The user in question
     * @param organization The organization we're considering
     * @return The set of permissions the user has for that organization
     */
    public Set<Permission> getUserPermissions(SafaUser user, Organization organization) {
        List<OrganizationRole> organizationRoles = getUserRoles(user, organization);

        Set<Permission> permissions = new HashSet<>();
        organizationRoles.forEach(role -> permissions.addAll(role.getGrants()));
        return permissions;
    }

    /**
     * Gets the list of roles a user has associated with a given project. Note that
     * just because a user has no role for a project does not mean they cannot access it,
     * as their team or organization role may give them additional permissions.
     *
     * @param user The user in question
     * @param project The project we're considering
     * @return The list of roles the user has associated with that project
     */
    public List<ProjectRole> getUserRoles(SafaUser user, Project project) {
        return projectMembershipService.getUserRoles(user, project);
    }

    /**
     * Gets the list of roles a user has associated with a given team. Note that
     * just because a user has no role for a team does not mean they cannot access it,
     * as their organization role may give them additional permissions.
     *
     * @param user The user in question
     * @param team The team we're considering
     * @return The list of roles the user has associated with that team
     */
    public List<TeamRole> getUserRoles(SafaUser user, Team team) {
        return teamMembershipService.getUserRoles(user, team);
    }

    /**
     * Gets the list of roles a user has associated with a given organization.
     *
     * @param user The user in question
     * @param organization The organization we're considering
     * @return The list of roles the user has associated with that organization
     */
    public List<OrganizationRole> getUserRoles(SafaUser user, Organization organization) {
        return orgMembershipService.getUserRoles(user, organization);
    }

}
