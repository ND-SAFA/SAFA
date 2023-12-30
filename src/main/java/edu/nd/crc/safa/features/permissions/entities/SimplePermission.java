package edu.nd.crc.safa.features.permissions.entities;

import edu.nd.crc.safa.features.permissions.checks.AdditionalPermissionCheck;
import edu.nd.crc.safa.features.permissions.checks.utility.NoAdditionalPermissionCheck;

/**
 * A simple permission is a permission that is just a name
 * and nothing else. This class is a functional interface, so
 * you can even create an ad-hoc permission as a lambda like this:
 *
 * <pre>
 * {@code
 *      throw new MissingPermissionException((SimplePermission) () -> "new.permission");
 * }
 * </pre>
 */
@FunctionalInterface
public interface SimplePermission extends Permission {
    @Override
    default AdditionalPermissionCheck getAdditionalCheck() {
        return new NoAdditionalPermissionCheck();
    }
}
