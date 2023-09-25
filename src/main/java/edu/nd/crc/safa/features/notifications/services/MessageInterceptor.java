package edu.nd.crc.safa.features.notifications.services;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import java.util.stream.Collectors;

import edu.nd.crc.safa.authentication.SafaUserDetails;
import edu.nd.crc.safa.config.ObjectMapperConfig;
import edu.nd.crc.safa.features.notifications.MemberNotification;
import edu.nd.crc.safa.features.notifications.NotificationMessage;
import edu.nd.crc.safa.features.notifications.VersionNotification;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.app.UserAppEntity;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.AllArgsConstructor;
import org.springframework.messaging.Message;
import org.springframework.messaging.MessageChannel;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.messaging.simp.stomp.StompCommand;
import org.springframework.messaging.simp.stomp.StompHeaderAccessor;
import org.springframework.messaging.support.ChannelInterceptor;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;


@AllArgsConstructor
public class MessageInterceptor implements ChannelInterceptor {

    private final ConcurrentHashMap<UUID, List<UserAppEntity>> userProjectMap = new ConcurrentHashMap<>();

    private static void sendToUser(SafaUser user, MessageChannel channel, Object object) {
        String userTopic = String.format("/user/%s/updates", user.getUserId());
        send(userTopic, channel, object);
    }

    private static void send(String topic, MessageChannel channel, Object object) {
        try {
            SimpMessagingTemplate simp = new SimpMessagingTemplate(channel);
            ObjectMapper mapper = ObjectMapperConfig.create();

            simp.convertAndSend(topic, mapper.writeValueAsBytes(object));
            System.out.println(String.format("%s -> %s", topic, object));
        } catch (Exception e) {
            e.printStackTrace();
            throw new RuntimeException(e);
        }
    }

    @Override
    public Message<?> preSend(Message<?> message, MessageChannel channel) {
        try {
            List<StompCommand> handleCommands = List.of(StompCommand.SUBSCRIBE,
                StompCommand.UNSUBSCRIBE,
                StompCommand.DISCONNECT);

            StompHeaderAccessor accessor = StompHeaderAccessor.wrap(message);
            StompCommand command = accessor.getCommand();
            if (command != null && handleCommands.contains(command)) {
                SafaUser user = getAuthenticatedUser(message);
                String destination = (String) message.getHeaders().get("simpDestination");

                if (command.equals(StompCommand.SUBSCRIBE)) {
                    onSubscribe(user, channel, destination);
                } else {
                    removeUser(user, channel);
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
        return message;
    }

    private void onSubscribe(SafaUser user, MessageChannel channel, String destination) {
        String[] parts = destination.split("/");
        if (parts[1].equals("user")) {
            System.out.printf("%s @ %s", user.getEmail(), destination);
            return;
        }
        String channelName = parts[2];
        String channelId = parts[3];
        NotificationMessage notification;
        switch (channelName) {
            case "project":
                UUID projectId = UUID.fromString(channelId);
                addUser(user, projectId);
                notification = new MemberNotification(this.userProjectMap.get(projectId));
                sendToUser(user, channel, notification);
                break;
            case "version":
                notification = new VersionNotification(new ProjectVersion());
                sendToUser(user, channel, notification);
                System.out.printf("%s @ %s%n", user.getEmail(), destination);
                break;
            default:
                System.out.println("oops");
                break;
        }
    }

    private SafaUser getAuthenticatedUser(Message message) {
        UsernamePasswordAuthenticationToken authentication = (UsernamePasswordAuthenticationToken) message
            .getHeaders()
            .get("simpSessionAttributes", ConcurrentHashMap.class)
            .get("simpUser");
        SafaUserDetails userDetails = (SafaUserDetails) authentication.getPrincipal();
        SafaUser user = userDetails.getUser();

        if (user == null) {
            throw new SafaError("User is not authorized.");
        }
        return user;
    }

    private void addUser(SafaUser user, UUID project) {
        if (!this.userProjectMap.contains(project)) {
            this.userProjectMap.put(project, new ArrayList<>());
        }
        List<UserAppEntity> projectUsers = this.userProjectMap.get(project);
        if (!projectUsers.contains(user)) {
            projectUsers.add(new UserAppEntity(user));
        }
    }

    private void removeUser(SafaUser user, MessageChannel channel) {
        this.userProjectMap.forEach((k, v) -> {
            List<UserAppEntity> users =
                v.stream().filter(u -> u.getUserId().equals(user.getUserId())).collect(Collectors.toList());

            if (v.removeAll(users)) {
                String projectTopic = String.format("/topic/project/%s", k);
                send(projectTopic, channel, v);
            }
        });
    }
}
