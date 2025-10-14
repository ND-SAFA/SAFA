package edu.nd.crc.safa.features.notifications.members;

import java.util.List;

import edu.nd.crc.safa.features.notifications.Topic;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;

import lombok.AllArgsConstructor;
import org.jetbrains.annotations.NotNull;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.messaging.Message;
import org.springframework.messaging.MessageChannel;
import org.springframework.messaging.simp.stomp.StompCommand;
import org.springframework.messaging.support.ChannelInterceptor;

/**
 * Requirements:
 * 1. On subscribe, store user, project, and subscription ID -> Notify project members of new active users ->
 * Acknoledge that user is subscribed.
 * 2. On un-subscribe, retrieve project from subscription ID and remove user -> Notify project members.
 * 3. On disconnect, remove user from all projects -> Notify all affected projects.
 * Design:
 * 1. on subscribe, map subscription ID to (user, project) AND add user to project members.
 */
@AllArgsConstructor
public class ActiveMembersInterceptor implements ChannelInterceptor {
    private static final List<StompCommand> commandsToHandle = List.of(StompCommand.SUBSCRIBE,
        StompCommand.UNSUBSCRIBE,
        StompCommand.DISCONNECT);
    private static final Logger log = LoggerFactory.getLogger(ActiveMembersInterceptor.class);
    private final ActiveMembersStore projectStore = new ActiveMembersStore();

    /**
     * Tracks subscriptions and disconnections to keep list of active users.
     *
     * @param message The message coming from general traffic.
     * @param channel The channel used to respond to events.
     * @param sent    Whether the message being processed has already sent.
     */
    @Override
    public void postSend(@NotNull Message<?> message, @NotNull MessageChannel channel, boolean sent) {
        try {
            MessageProxy proxy = new MessageProxy(message, channel);
            if (sent && proxy.hasCommand(commandsToHandle)) {
                handleMessage(proxy);
            }
        } catch (Exception e) {
            log.error("Active member interceptor failed.", e);
        }
    }

    /**
     * Handles requirements for keeping track of active users.
     *
     * @param proxy The message proxy used to interact with websocket server.
     */
    private void handleMessage(MessageProxy proxy) {
        if (proxy.isCommand(StompCommand.SUBSCRIBE)) {
            if (proxy.isTopic(Topic.PROJECT)) {
                projectStore.subscribe(new ProjectSubscriptionMessage(proxy));
            }
        } else if (proxy.isCommand(StompCommand.UNSUBSCRIBE)) {
            projectStore.unsubscribe(proxy.getSubscriptionId(), proxy.getMessageChannel());
        } else if (proxy.isCommand(StompCommand.DISCONNECT)) {
            projectStore.disconnect(proxy.getUser(), proxy.getMessageChannel());
        } else {
            throw new SafaError("Unhandled stomp command:" + proxy.getCommand());
        }
    }
}

