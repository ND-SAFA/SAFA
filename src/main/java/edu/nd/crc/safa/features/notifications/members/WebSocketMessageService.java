package edu.nd.crc.safa.features.notifications.members;

import java.util.List;
import java.util.Map;
import java.util.UUID;

import edu.nd.crc.safa.authentication.SafaUserDetails;
import edu.nd.crc.safa.config.ObjectMapperConfig;
import edu.nd.crc.safa.features.notifications.TopicCreator;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.IUser;
import edu.nd.crc.safa.features.users.entities.app.UserAppEntity;

import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import org.springframework.messaging.Message;
import org.springframework.messaging.MessageChannel;
import org.springframework.messaging.MessageHeaders;
import org.springframework.messaging.simp.SimpMessageHeaderAccessor;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;

@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class WebSocketMessageService {
    /**
     * Returns the destination of the message.
     *
     * @param message The message sent to a destination.
     * @return String representing destination.
     */
    public static String getDestination(Message message) {
        MessageHeaders messageHeaders = message.getHeaders();
        String destination = messageHeaders.get(SimpMessageHeaderAccessor.DESTINATION_HEADER, String.class);
        if (destination == null) {
            throw new SafaError("Unknown destination on message.\n" + message);
        }
        return destination;
    }

    /**
     * Extracts the subscription ID from unsubscribe message.
     *
     * @param message The message containing subscription ID.
     * @return String representing subscription Id.
     */
    public static String getSubscriptionIdFromUnsubcribeMessage(Message message) {
        MessageHeaders headers = message.getHeaders();
        Map nativeHeaderMap = headers.get(SimpMessageHeaderAccessor.NATIVE_HEADERS, Map.class);
        List<String> ids = (List<String>) nativeHeaderMap.get("id");
        if (ids.size() > 1) {
            throw new SafaError("Expected single id in message but found multiple: " + ids);
        }
        return ids.get(0);
    }

    /**
     * Extracts user established during Stomp connection.
     *
     * @param message The message sent by the user.
     * @return IUser associated with sender.
     */
    public static IUser getUserFromAuthenticatedMessage(Message message) {
        MessageHeaders messageHeaders = message.getHeaders();
        UsernamePasswordAuthenticationToken userAuthenticationToken =
            messageHeaders.get(SimpMessageHeaderAccessor.USER_HEADER,
                UsernamePasswordAuthenticationToken.class);
        SafaUserDetails safaUserDetails = (SafaUserDetails) userAuthenticationToken.getPrincipal();
        return new UserAppEntity(safaUserDetails.getUser());
    }

    /**
     * Sends message to project topic.
     *
     * @param projectId The ID of the project to send message to.
     * @param channel   The channel used to send message.
     * @param object    The object to send through channel.
     */
    public static void sendToProject(UUID projectId, MessageChannel channel, Object object) {
        String topic = TopicCreator.getProjectTopic(projectId);
        send(topic, channel, object);
    }

    /**
     * Sends message to topic over channel.
     *
     * @param topic   The topic to send message to.
     * @param channel The channel to send the message through.
     * @param message The data to send in message.
     */
    private static void send(String topic, MessageChannel channel, Object message) {
        try {
            SimpMessagingTemplate simp = new SimpMessagingTemplate(channel);
            ObjectMapper mapper = ObjectMapperConfig.create();
            simp.convertAndSend(topic, mapper.writeValueAsBytes(message));
        } catch (Exception e) {
            e.printStackTrace();
            throw new RuntimeException(e);
        }
    }
}
