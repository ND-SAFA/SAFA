package edu.nd.crc.safa.config;

import edu.nd.crc.safa.features.notifications.members.ActiveMembersInterceptor;

import lombok.AllArgsConstructor;
import org.springframework.context.annotation.Configuration;
import org.springframework.messaging.simp.config.ChannelRegistration;
import org.springframework.messaging.simp.config.MessageBrokerRegistry;
import org.springframework.web.socket.config.annotation.StompEndpointRegistry;
import org.springframework.web.socket.config.annotation.WebSocketMessageBrokerConfigurer;
import org.springframework.web.socket.config.annotation.WebSocketTransportRegistration;

/**
 * Configures the general WebSocket configurations including:
 * - endpoint for initial connects to websockets
 * - setting message size
 * - setting the topic and individual message endpoints.
 */
@AllArgsConstructor
@Configuration
public class WebSocketBrokerConfig implements WebSocketMessageBrokerConfigurer {
    public static final int MESSAGE_SIZE_LIMIT = 50 * 1024 * 1024;

    @Override
    public void configureClientInboundChannel(ChannelRegistration registration) {
        ActiveMembersInterceptor activeMembersInterceptor = new ActiveMembersInterceptor();
        registration.interceptors(activeMembersInterceptor);
    }

    @Override
    public void configureWebSocketTransport(WebSocketTransportRegistration registration) {
        registration.setMessageSizeLimit(MESSAGE_SIZE_LIMIT); // default : 64 * 1024
        registration.setSendBufferSizeLimit(MESSAGE_SIZE_LIMIT); // default : 512 * 1024
    }

    @Override
    public void configureMessageBroker(MessageBrokerRegistry config) {
        config.enableSimpleBroker("/topic", "/user");
        config.setUserDestinationPrefix("/user");
        config.setApplicationDestinationPrefixes("/app");
    }

    @Override
    public void registerStompEndpoints(StompEndpointRegistry registry) {
        registry
            .addEndpoint("/websocket")
            .setAllowedOriginPatterns("*")
            .withSockJS()
        ;
    }
}
