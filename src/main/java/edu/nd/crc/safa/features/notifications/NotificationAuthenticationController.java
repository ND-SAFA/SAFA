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
    public void authenticateUser(AuthenticationMessage incomingMessage, SimpMessageHeaderAccessor accessor) {
        System.out.println("ATTENTION:" + incomingMessage);
        String token = incomingMessage.getToken();
        Object outgoingMessage;
        if (token == null || token.isEmpty()) {
            ErrorMessage errorMessage = new ErrorMessage();
            errorMessage.setMessage("Token is null or empty, invalid token.");
            outgoingMessage = errorMessage;
        }
        try {
            UserAppEntity user = authorizationService.getUser(token);
            outgoingMessage = new AcknowledgeMessage("OK");
            Map<String, Object> sessionAttributes = getSessionAttributes(accessor);
            sessionAttributes.put(SimpMessageHeaderAccessor.USER_HEADER, user);
            notificationService.sendToUser(user, outgoingMessage);
        } catch (Exception e) {
            outgoingMessage = new ErrorMessage(e.getMessage());
        }
    }

    @MessageMapping("/chat")
    public void chat(ChatMessage message, SimpMessageHeaderAccessor accessor) {
        UserAppEntity user = getUser(accessor);
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
        return (UserAppEntity) sessionAttributes.get(SimpMessageHeaderAccessor.USER_HEADER);
    }
}
