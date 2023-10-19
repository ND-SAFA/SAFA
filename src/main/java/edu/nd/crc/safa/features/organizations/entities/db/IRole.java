package edu.nd.crc.safa.features.organizations.entities.db;

import java.util.Set;

import edu.nd.crc.safa.features.permissions.entities.Permission;

/**
 * This is a generic interface for roles
 *
 * @see OrganizationRole
 * @see TeamRole
 * @see ProjectRole
 */
public interface IRole {
    /**
     * Get the permissions granted by this role
     *
     * @return The permissions this role grants
     */
    Set<Permission> getGrants();

    /**
     * Get the name of the role
     *
     * @return The role name
     */
    String name();
}
