package edu.nd.crc.safa.features.chat.entities.persistent;

import lombok.AccessLevel;
import lombok.AllArgsConstructor;

@AllArgsConstructor(access = AccessLevel.PRIVATE)
public enum ChatSharePermission {
    READ(0),
    EDIT(1);

    private final int level;

    /**
     * Returns whether permission is sufficiently high enough for requested permission.
     *
     * @param requestedPermission Permission expected to be met.
     * @return True if permission is met.
     */
    public boolean hasPermission(ChatSharePermission requestedPermission) {
        return requestedPermission.level >= this.level;
    }
}
