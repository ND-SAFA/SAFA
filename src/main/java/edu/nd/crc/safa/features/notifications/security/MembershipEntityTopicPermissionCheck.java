package edu.nd.crc.safa.features.notifications.security;

import java.util.UUID;
import java.util.function.Function;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.notifications.members.DestinationPath;
import edu.nd.crc.safa.features.organizations.entities.db.IEntityWithMembership;
import edu.nd.crc.safa.features.permissions.entities.Permission;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.AllArgsConstructor;

/**
 * Topic permission check for topics corresponding to implementations of {@link IEntityWithMembership}
 */
@AllArgsConstructor
public class MembershipEntityTopicPermissionCheck implements TopicPermissionCheckFunction {

    private final Permission permission;
    private final Function<UUID, IEntityWithMembership> retrievalFunction;

    @Override
    public boolean canSubscribe(SafaUser user, DestinationPath destinationPath) {
        UUID id = destinationPath.getTopicId();
        IEntityWithMembership entity = retrievalFunction.apply(id);
        return ServiceProvider.getInstance().getPermissionService().hasPermission(permission, entity, user);
    }
}
