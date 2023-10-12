package edu.nd.crc.safa.features.notifications.services;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.notifications.AcknowledgeMessage;
import edu.nd.crc.safa.features.notifications.WebSocketMessageService;
import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.notifications.entities.NotificationAction;
import edu.nd.crc.safa.features.notifications.entities.NotificationEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.IUser;
import edu.nd.crc.safa.features.users.entities.app.UserAppEntity;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.repositories.SafaUserRepository;

import lombok.AllArgsConstructor;
import lombok.Data;
import org.springframework.messaging.Message;
import org.springframework.messaging.MessageChannel;
import org.springframework.messaging.simp.SimpMessageHeaderAccessor;
import org.springframework.messaging.simp.stomp.StompCommand;
import org.springframework.messaging.simp.stomp.StompHeaderAccessor;
import org.springframework.messaging.support.ChannelInterceptor;

@AllArgsConstructor
public class MessageInterceptor implements ChannelInterceptor {

    private final SafaUserRepository userRepository;

    private final ConcurrentHashMap<UUID, List<IUser>> userProjectMap = new ConcurrentHashMap<>();

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
            DestinationPath path = new DestinationPath(destination);

            if (path.isChannel("user")) {
                authenticateUser(path, channel, accessor);
            } else {
                IUser user = WebSocketMessageService.getUserFromAuthenticatedMessage(message);
                onSubscribe(user, channel, path);
            }
        } else {
            System.out.println("OTHER MESSAGE:" + message);
            IUser user = WebSocketMessageService.getUserFromAuthenticatedMessage(message);
            removeUser(user, channel);
        }
    }

    private void authenticateUser(DestinationPath path, MessageChannel channel, StompHeaderAccessor accessor) {
        UUID userId = path.getChannelId();
        Optional<SafaUser> userOptional = this.userRepository.findById(userId);

        if (userOptional.isEmpty()) {
            String error = String.format("Unable to find user with id {%s}.", userId);
            throw new SafaError(error);
        }
        UserAppEntity user = new UserAppEntity(userOptional.get());
        Map<String, Object> sessionAttributes = accessor.getSessionAttributes();
        sessionAttributes.put(SimpMessageHeaderAccessor.USER_HEADER, user);
        System.out.println("AUTHENTICATED USER: " + user.getEmail());
        WebSocketMessageService.sendToUser(user, channel, new AcknowledgeMessage("Authenticated."));
    }

    private void onSubscribe(IUser user, MessageChannel channel, DestinationPath path) {
        if (path.isChannel("project")) {
            UUID channelId = path.getChannelId();
            addUser(user, channelId);
            List<IUser> activeProjectUsers = this.userProjectMap.get(channelId);
            Change change = createChange(activeProjectUsers);
            EntityChangeMessage message = new EntityChangeMessage(user, change);
            WebSocketMessageService.sendToProject(channelId, channel, message);
        }
        String msg = String.format("%s @ %s", user.getEmail(), path.getChannelName());
        WebSocketMessageService.sendToUser(user, channel, new AcknowledgeMessage(msg));
    }

    private void addUser(IUser user, UUID project) {
        this.userProjectMap.computeIfAbsent(project, projectId -> new ArrayList<>());
        List<IUser> projectUsers = this.userProjectMap.get(project);
        if (!projectUsers.contains(user)) {
            projectUsers.add(user);
        }
    }

    private void removeUser(IUser user, MessageChannel channel) {
        this.userProjectMap.forEach((k, v) -> {
            List<IUser> users =
                v.stream().filter(u -> u.getUserId().equals(user.getUserId())).collect(Collectors.toList());

            if (v.removeAll(users)) {
                String projectTopic = String.format("/topic/project/%s", k);
                Change newActiveMembers = createChange(v);
                EntityChangeMessage message = new EntityChangeMessage(user, newActiveMembers);
                WebSocketMessageService.send(projectTopic, channel, message);
            }
        });
    }

    private Change createChange(List<IUser> activeUsers) {
        Change change = new Change();
        change.setAction(NotificationAction.UPDATE);
        change.setEntities(activeUsers);
        change.setEntity(NotificationEntity.ACTIVE_MEMBERS);
        return change;
    }
}

@Data
class DestinationPath {
    private final String channelName;
    private final UUID channelId;

    public DestinationPath(String path) {
        String[] parts = path.split("/");
        if (parts[1].equals("topic")) {
            this.channelName = parts[2];
            this.channelId = UUID.fromString(parts[3]);
        } else {
            this.channelName = parts[1];
            this.channelId = UUID.fromString(parts[2]);
        }
    }

    public boolean isChannel(String channelName) {
        return this.channelName.equals(channelName);
    }
}
