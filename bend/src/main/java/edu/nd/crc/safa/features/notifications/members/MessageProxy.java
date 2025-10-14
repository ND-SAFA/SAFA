package edu.nd.crc.safa.features.notifications.members;

import java.util.List;

import edu.nd.crc.safa.features.notifications.Topic;
import edu.nd.crc.safa.features.users.entities.IUser;

import lombok.Data;
import org.springframework.messaging.Message;
import org.springframework.messaging.MessageChannel;
import org.springframework.messaging.simp.stomp.StompCommand;
import org.springframework.messaging.simp.stomp.StompHeaderAccessor;

/**
 * Creates unified websocket API.
 */
@Data
public class MessageProxy {
    /**
     * The message being processed.
     */
    private final Message<?> message;
    /**
     * The message channel used to send other messages back.
     */
    private final MessageChannel messageChannel;
    /**
     * The stomp command associated with message.
     */
    private final StompCommand command;

    public MessageProxy(Message<?> message, MessageChannel messageChannel) {
        this.message = message;
        this.messageChannel = messageChannel;
        this.command = StompHeaderAccessor.wrap(message).getCommand();
    }

    /**
     * Whether message command is contained within list.
     *
     * @param commands List of possible commands to match.
     * @return Whether message command is within list.
     */
    public boolean hasCommand(List<StompCommand> commands) {
        return this.command != null && commands.contains(this.command);
    }

    /**
     * Whether message exactly matches command.
     *
     * @param command The command to check against messages'.
     * @return True if command matches that of message.
     */
    public boolean isCommand(StompCommand command) {
        return hasCommand(List.of(command));
    }

    /**
     * Returns the destination of the message if it exists. (e.g. DISCONNECT has no destination).
     *
     * @return DestinationPath containing information about where the message is going.
     */
    public DestinationPath getDestination() {
        String destination = WebSocketMessageService.getDestination(this.message);
        return new DestinationPath(destination);
    }

    /**
     * Shortcut method for check if the destination of the message has the topic name.
     *
     * @param topic The topic to check if the message is heading to.
     * @return True if message heading to destination in topic.
     */
    public boolean isTopic(Topic topic) {
        return getDestination().isTopic(topic);
    }

    /**
     * Returns the subscription ID associated with message. Only valid if message is related to a subscription.
     *
     * @return The ID of subscription.
     */
    public String getSubscriptionId() {
        return WebSocketMessageService.getSubscriptionIdFromUnsubcribeMessage(message);
    }

    /**
     * Extracts the user authenticated with web socket connection.
     *
     * @return The user.
     */
    public IUser getUser() {
        return WebSocketMessageService.getUserFromAuthenticatedMessage(message);
    }
}
