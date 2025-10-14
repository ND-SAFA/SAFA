package edu.nd.crc.safa.features.permissions.entities;

import edu.nd.crc.safa.features.permissions.checks.AdditionalPermissionCheck;

/**
 * <p>A permission is effectively just a string that is associated with
 * a user within some context, such as a project or organization. If
 * the user has the permission associated with their account, that grants
 * them the ability to perform an action.</p>
 * <br/>
 * <p>Additionally, permissions can have additional checks associated with
 * them. If that is the case, it means that having the permission is not
 * enough to grant the user the ability to perform the action, and they
 * must also pass some other check. These checks can be just about anything,
 * for instance checking that an organization is paying for a feature.</p>
 *
 * @see AdditionalPermissionCheck
 * @see edu.nd.crc.safa.features.permissions.services.PermissionService
 * @see SimplePermission
 * @see ProjectPermission
 * @see TeamPermission
 * @see OrganizationPermission
 */
public interface Permission {
    /**
     * <p>Get the name of the permission. This should be in the form
     * {@code 'context.name'}.</p>
     * <br/>
     * <p>For example, a permission that grants a user to remove
     * all other users from an organization might be called
     * {@code 'org.remove_all_users'}. Ultimately, though, it is
     * just a string and can be anything.</p>
     *
     * @return The permission's name
     */
    String getName();

    /**
     * Get additional check associated with this permission.
     *
     * @return Additional check for this permission.
     */
    AdditionalPermissionCheck getAdditionalCheck();
}
