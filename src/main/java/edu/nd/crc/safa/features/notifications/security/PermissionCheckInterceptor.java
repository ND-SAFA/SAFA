package edu.nd.crc.safa.features.notifications.security;

import java.util.Map;
import java.util.Set;

import edu.nd.crc.safa.features.common.ServiceProvider;
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

public class PermissionCheckInterceptor implements ChannelInterceptor {

    /**
     * Set of topics that do not need any security checks
     */
    private static final Set<String> unsecuredTopics = Set.of(
            "users"
    );

    /**
     * Defines how to check for permissions for each secured topic
     */
    private static final Map<String, TopicPermissionCheckFunction> securedTopics = Map.of(
            "version", new MembershipEntityTopicPermissionCheck(id -> sp().getVersionService().getVersionById(id)),
            "project", new MembershipEntityTopicPermissionCheck(id -> sp().getProjectService().getProjectById(id)),
            "jobs", new JobTopicPermissionCheck()
    );

    private static final Logger logger = LoggerFactory.getLogger(PermissionCheckInterceptor.class);

    /**
     * Shortened name for {@link ServiceProvider#getInstance()}
     *
     * @return The service provider instance
     */
    private static ServiceProvider sp() {
        return ServiceProvider.getInstance();
    }

    @Override
    public Message<?> preSend(@NotNull Message<?> message, @NotNull MessageChannel channel) {
        MessageProxy proxy = new MessageProxy(message, channel);
        if (!proxy.isCommand(StompCommand.SUBSCRIBE)) {
            return message;
        }

        IUser user = proxy.getUser();
        DestinationPath path = proxy.getDestination();
        String topic = path.getTopic();

        if (unsecuredTopics.contains(topic)) {
            return message;
        }

        assert securedTopics.containsKey(topic) : String.format("Unknown topic \"%s\". Please specify how it should"
                + "be secured in %s", topic, PermissionCheckInterceptor.class.getName());

        TopicPermissionCheckFunction permissionCheckFunction = securedTopics.get(topic);

        if (permissionCheckFunction.canSubscribe(getSafaUser(user), proxy.getDestination())) {
            return message;
        } else {
            logger.warn("Attempt by {} to subscribe to {} which they do not have permission to view",
                    user.getEmail(), path);
            return null;
        }
    }

    private SafaUser getSafaUser(IUser iUser) {
        return ServiceProvider.getInstance().getSafaUserService().getUserById(iUser.getUserId());
    }
}
