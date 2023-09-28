package edu.nd.crc.safa.features.notifications;

import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

import edu.nd.crc.safa.config.ObjectMapperConfig;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.app.UserAppEntity;

import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import org.springframework.messaging.Message;
import org.springframework.messaging.MessageChannel;
import org.springframework.messaging.MessageHeaders;
import org.springframework.messaging.simp.SimpMessageHeaderAccessor;
import org.springframework.messaging.simp.SimpMessagingTemplate;

@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class WebSocketMessageService {
    public static String getDestination(Message message) {
        MessageHeaders messageHeaders = message.getHeaders();
        String destination = messageHeaders.get(SimpMessageHeaderAccessor.DESTINATION_HEADER, String.class);
        if (destination == null) {
            throw new SafaError("Unknown destination.");
        }
        return destination;
    }

    public static UserAppEntity getUser(Message message) {
        MessageHeaders messageHeaders = message.getHeaders();
        ConcurrentHashMap attributes = messageHeaders.get(SimpMessageHeaderAccessor.SESSION_ATTRIBUTES, ConcurrentHashMap.class);
        if (attributes == null) {
            throw new SafaError("Session attributes are empty. Has the user authenticated?");
        }
        UserAppEntity user = (UserAppEntity) attributes.get(SimpMessageHeaderAccessor.USER_HEADER);
        if (user == null) {
            throw new SafaError("Session has no user. Has the user authenticated?");
        }
        return user;
    }

    public static void sendToProject(UUID projectId, MessageChannel channel, Object object) {
        String topic = TopicCreator.getProjectTopic(projectId);
        send(topic, channel, object);
    }

    public static void send(String topic, MessageChannel channel, Object object) {
        try {
            SimpMessagingTemplate simp = new SimpMessagingTemplate(channel);
            ObjectMapper mapper = ObjectMapperConfig.create();

            simp.convertAndSend(topic, mapper.writeValueAsBytes(object));
            System.out.printf("%s -> %s%n", topic, object);
        } catch (Exception e) {
            e.printStackTrace();
            throw new RuntimeException(e);
        }
    }
}
