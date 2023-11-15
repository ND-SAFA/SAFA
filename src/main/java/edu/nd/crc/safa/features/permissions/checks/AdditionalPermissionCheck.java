package edu.nd.crc.safa.features.permissions.checks;

/**
 * Interface for additional checks that can be tied to permissions
 */
@FunctionalInterface
public interface AdditionalPermissionCheck {
    /**
     * Perform the check
     *
     * @param context Context variable which contains data that might be useful for doing the check
     * @return Whether the check passed
     */
    boolean doCheck(PermissionCheckContext context);
}
