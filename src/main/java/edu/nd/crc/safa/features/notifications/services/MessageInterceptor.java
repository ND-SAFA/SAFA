package edu.nd.crc.safa.features.notifications.services;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.notifications.WebSocketMessageService;
import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.notifications.entities.NotificationAction;
import edu.nd.crc.safa.features.notifications.entities.NotificationEntity;
import edu.nd.crc.safa.features.users.entities.app.UserAppEntity;

import lombok.AllArgsConstructor;
import org.springframework.messaging.Message;
import org.springframework.messaging.MessageChannel;
import org.springframework.messaging.simp.stomp.StompCommand;
import org.springframework.messaging.simp.stomp.StompHeaderAccessor;
import org.springframework.messaging.support.ChannelInterceptor;


@AllArgsConstructor
public class MessageInterceptor implements ChannelInterceptor {

    private final ConcurrentHashMap<UUID, List<UserAppEntity>> userProjectMap = new ConcurrentHashMap<>();

    @Override
    public void postSend(Message<?> message, MessageChannel channel, boolean sent) {
        List<StompCommand> handleCommands = List.of(StompCommand.SUBSCRIBE,
            StompCommand.UNSUBSCRIBE,
            StompCommand.DISCONNECT);

        StompHeaderAccessor accessor = StompHeaderAccessor.wrap(message);
        StompCommand command = accessor.getCommand();
        if (!sent || command == null || !handleCommands.contains(command)) {
            return;
        }

        if (command.equals(StompCommand.SUBSCRIBE)) {
            String destination = WebSocketMessageService.getDestination(message);
            if (destination.startsWith("/user")) {
                return;
            }
            UserAppEntity user = WebSocketMessageService.getUser(message);
            onSubscribe(user, channel, destination);
        } else {
            UserAppEntity user = WebSocketMessageService.getUser(message);
            removeUser(user, channel);
        }
    }

    private void onSubscribe(UserAppEntity user, MessageChannel channel, String destination) {
        String[] parts = destination.split("/");
        if (parts[1].equals("user")) {
            return;
        }
        String channelName = parts[2];
        String channelId = parts[3];
        if (channelName.equals("project")) {
            UUID projectId = UUID.fromString(channelId);
            addUser(user, projectId);

            List<UserAppEntity> activeProjectUsers = this.userProjectMap.get(projectId);
            Change change = createChange(activeProjectUsers);
            EntityChangeMessage message = new EntityChangeMessage(user, change);
            WebSocketMessageService.sendToProject(projectId, channel, message);
        }
    }

    private void addUser(UserAppEntity user, UUID project) {
        this.userProjectMap.computeIfAbsent(project, projectId -> new ArrayList<>());
        List<UserAppEntity> projectUsers = this.userProjectMap.get(project);
        if (!projectUsers.contains(user)) {
            projectUsers.add(user);
        }
    }

    private void removeUser(UserAppEntity user, MessageChannel channel) {
        this.userProjectMap.forEach((k, v) -> {
            List<UserAppEntity> users =
                v.stream().filter(u -> u.getUserId().equals(user.getUserId())).collect(Collectors.toList());

            if (v.removeAll(users)) {
                String projectTopic = String.format("/topic/project/%s", k);
                WebSocketMessageService.send(projectTopic, channel, v);
            }
        });
    }

    private Change createChange(List<UserAppEntity> activeUsers) {
        Change change = new Change();
        change.setAction(NotificationAction.UPDATE);
        change.setEntities(activeUsers);
        change.setEntity(NotificationEntity.ACTIVE_MEMBERS);
        return change;
    }
}
