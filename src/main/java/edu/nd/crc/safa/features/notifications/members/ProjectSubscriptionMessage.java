package edu.nd.crc.safa.features.notifications.members;

import java.util.UUID;

import edu.nd.crc.safa.features.users.entities.IUser;

import lombok.Data;
import org.springframework.messaging.MessageChannel;

/**
 * Creates data structure for handling state of active project members.
 */
@Data
public class ProjectSubscriptionMessage {
    /**
     * The ID related to the project subscription.
     */
    private final String subscriptionId;
    /**
     * The user subscribed to the project.
     */
    private final IUser user;
    /**
     * The ID of the project subscribed to.
     */
    private final UUID projectId;
    /**
     * The message channel used to send messages to projects.
     */
    private final MessageChannel messageChannel;

    public ProjectSubscriptionMessage(MessageProxy proxy) {
        this.subscriptionId = proxy.getSubscriptionId();
        this.user = proxy.getUser();
        this.projectId = proxy.getDestination().getTopicId();
        this.messageChannel = proxy.getMessageChannel();
    }
}
