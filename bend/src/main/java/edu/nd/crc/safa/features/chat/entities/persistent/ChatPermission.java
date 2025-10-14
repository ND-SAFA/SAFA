package edu.nd.crc.safa.features.chat.entities.persistent;

import edu.nd.crc.safa.features.permissions.checks.AdditionalPermissionCheck;
import edu.nd.crc.safa.features.permissions.entities.Permission;

import lombok.AccessLevel;
import lombok.AllArgsConstructor;

@AllArgsConstructor(access = AccessLevel.PRIVATE)
public enum ChatPermission implements Permission {
    READ(0),
    EDIT(1),
    OWNER(2);

    /**
     * Value used to compare priviledges.
     */
    private final int level;

    /**
     * Returns whether permission is sufficiently high enough for requested permission.
     *
     * @param requestedPermission Permission expected to be met.
     * @return True if permission is met.
     */
    public boolean hasPermission(ChatPermission requestedPermission) {
        return requestedPermission.level >= this.level;
    }

    /**
     * @return Name of permission level.
     */
    @Override
    public String getName() {
        return this.name();
    }

    /**
     * @return null, no additional check required.
     */
    @Override
    public AdditionalPermissionCheck getAdditionalCheck() {
        return null;
    }
}
