package edu.nd.crc.safa.features.permissions.entities;

import java.util.List;

/**
 * A simple permission is a permission that is just a name
 * and nothing else. This class is a functional interface, so
 * you can even create an ad-hoc permission as a lambda like this:
 *
 * <pre>
 * {@code
 *      () -> 'new.permission'
 * }
 * </pre>
 */
@FunctionalInterface
public interface SimplePermission extends Permission {
    @Override
    default List<AdditionalPermissionCheck> getAdditionalChecks() {
        return List.of();
    }
}
