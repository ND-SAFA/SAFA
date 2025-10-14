package edu.nd.crc.safa.features.permissions.checks;

/**
 * Interface for additional checks that can be tied to permissions. Broadly speaking,
 * implementations of this interface will be called like this:<br/>
 * <pre>
 * {@code
 *   AdditionalPermissionCheck check = ...;
 *   if (!check.doCheck(context)) {
 *     throw new RuntimeException(check.getMessage());
 *   }
 * }
 * </pre>
 */
public interface AdditionalPermissionCheck {
    /**
     * Perform the check
     *
     * @param context Context variable which contains data that might be useful for doing the check
     * @return Whether the check passed
     */
    boolean doCheck(PermissionCheckContext context);

    /**
     * Get the message that should be displayed if the check fails
     *
     * @return The message
     */
    String getMessage();

    /**
     * Specifies whether a superuser can override this check.
     *
     * @return True if this check can be overridden by an active superuser
     */
    boolean superuserCanOverride();
}
