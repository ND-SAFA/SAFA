package edu.nd.crc.safa.features.notifications.security;

import edu.nd.crc.safa.features.notifications.members.DestinationPath;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

@FunctionalInterface
public interface TopicPermissionCheckFunction {
    boolean canSubscribe(SafaUser user, DestinationPath destinationPath);
}
