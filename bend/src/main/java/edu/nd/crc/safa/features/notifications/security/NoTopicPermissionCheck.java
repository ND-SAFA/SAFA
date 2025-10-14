package edu.nd.crc.safa.features.notifications.security;

import edu.nd.crc.safa.features.notifications.members.DestinationPath;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

/**
 * No permission check needed. Always returns true.
 */
public class NoTopicPermissionCheck implements TopicPermissionCheckFunction {
    @Override
    public boolean canSubscribe(SafaUser user, DestinationPath destinationPath) {
        return true;
    }
}
