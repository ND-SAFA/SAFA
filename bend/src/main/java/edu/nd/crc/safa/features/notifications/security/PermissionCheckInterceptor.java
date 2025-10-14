package edu.nd.crc.safa.features.notifications.security;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.notifications.Topic;
import edu.nd.crc.safa.features.notifications.members.DestinationPath;
import edu.nd.crc.safa.features.notifications.members.MessageProxy;
import edu.nd.crc.safa.features.users.entities.IUser;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import org.jetbrains.annotations.NotNull;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.messaging.Message;
import org.springframework.messaging.MessageChannel;
import org.springframework.messaging.simp.stomp.StompCommand;
import org.springframework.messaging.support.ChannelInterceptor;

/**
 * <p>Intercepts subscription confirmation messages before they are sent to the user
 * and verifies that the user has permission to subscribe to that topic. If they do
 * not, the subscription confirmation message is not sent, which keeps the user from
 * being able to subscribe to that topic.</p>
 *
 * <p>Topic permissions are checked using {@link TopicPermissionCheckFunction}s, which
 * are attached to the corresponding topic in {@link Topic}.</p>
 */
public class PermissionCheckInterceptor implements ChannelInterceptor {

    private static final Logger logger = LoggerFactory.getLogger(PermissionCheckInterceptor.class);

    /**
     * Intercepts subscribe messages before they are sent to a channel. If the user does not have permission
     * to subscribe to that topic, the message is set to {@code null}, preventing it from being sent, which in turn
     * prevents the user from actually subscribing to the topic.
     *
     * @param message The message that is going to be sent. If it is not a subscribe message, it is ignored
     * @param channel The channel that the message is being sent to. This function does not use this argument
     * @return {@code null} if the message is a subscribe message and the user does not have permission to
     *         subscribe to that topic. Otherwise, the original message is returned.
     */
    @Override
    public Message<?> preSend(@NotNull Message<?> message, @NotNull MessageChannel channel) {
        MessageProxy proxy = new MessageProxy(message, channel);
        if (!proxy.isCommand(StompCommand.SUBSCRIBE)) {
            return message;
        }

        IUser user = proxy.getUser();
        DestinationPath path = proxy.getDestination();
        String topicName = path.getTopic();

        Topic topic = Topic.fromName(topicName);

        assert topic != null : String.format("Unknown topic \"%s\". Please specify how it should be secured in %s",
                topicName, Topic.class.getName());

        TopicPermissionCheckFunction permissionCheckFunction = topic.getPermissionFunctionSupplier().get();

        if (canSubscribe(getSafaUser(user), path, permissionCheckFunction)) {
            return message;
        } else {
            logger.warn("Attempt by {} to subscribe to {} which they do not have permission to view",
                    user.getEmail(), path);
            return null;
        }
    }

    /**
     * Checks if the given user can subscribe to the topic given by the path argument. This function
     * is just a wrapper around {@link TopicPermissionCheckFunction#canSubscribe(SafaUser, DestinationPath)}
     * which catches any exceptions that may occur.
     *
     * @param user The user attempting to subscribe
     * @param path The path of the topic the user is attempting to subscribe to
     * @param permissionFunction The function which will determine if the user can subscribe to this topic
     * @return True if the function succeeded and returned true, false otherwise
     */
    private boolean canSubscribe(IUser user, DestinationPath path, TopicPermissionCheckFunction permissionFunction) {
        try {
            return permissionFunction.canSubscribe(getSafaUser(user), path);
        } catch (Exception e) {
            logger.info("Error checking if user can subscribe to topic. User: {}, topic: {}, error: {}",
                    user.getEmail(), path, e.getMessage());
            return false;
        }
    }

    /**
     * Get the {@link SafaUser} associated with an {@link IUser}
     *
     * @param iUser A generic user definition
     * @return The {@link SafaUser} for the given {@link IUser}
     */
    private SafaUser getSafaUser(IUser iUser) {
        if (iUser instanceof SafaUser) {
            return (SafaUser) iUser;
        }
        return ServiceProvider.getInstance().getSafaUserService().getUserById(iUser.getUserId());
    }
}
