package edu.nd.crc.safa.features.notifications;

import java.util.Map;

import edu.nd.crc.safa.authentication.AuthorizationService;
import edu.nd.crc.safa.features.notifications.services.NotificationService;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.app.UserAppEntity;

import lombok.AllArgsConstructor;
import org.springframework.messaging.handler.annotation.MessageMapping;
import org.springframework.messaging.simp.SimpMessageHeaderAccessor;
import org.springframework.stereotype.Controller;

@AllArgsConstructor
@Controller
public class NotificationAuthenticationController {
    private final AuthorizationService authorizationService;
    private final NotificationService notificationService;

    @MessageMapping("/auth")
    public void authenticateUser(AuthenticationMessage message, SimpMessageHeaderAccessor accessor) {
        UserAppEntity user = authorizationService.getUser(message.getToken());
        Map<String, Object> sessionAttributes = getSessionAttributes(accessor);
        sessionAttributes.put(SimpMessageHeaderAccessor.USER_HEADER, user);
        notificationService.sendToUser(user, new AcknowledgeMessage("OK"));
    }

    @MessageMapping("/chat")
    public void chat(ChatMessage message, SimpMessageHeaderAccessor accessor) {
        UserAppEntity user = getUser(accessor);
        System.out.println(message.getMessage() + ":" + user.getEmail());
    }


    public Map<String, Object> getSessionAttributes(SimpMessageHeaderAccessor accessor) {
        Map<String, Object> sessionAttributes = accessor.getSessionAttributes();
        if (sessionAttributes == null) {
            throw new SafaError("Unable to access session attributes.");
        }
        return sessionAttributes;
    }

    public UserAppEntity getUser(SimpMessageHeaderAccessor accessor) {
        Map<String, Object> sessionAttributes = getSessionAttributes(accessor);
        UserAppEntity user =
            (UserAppEntity) sessionAttributes.get(SimpMessageHeaderAccessor.USER_HEADER);
        return user;
    }
}
