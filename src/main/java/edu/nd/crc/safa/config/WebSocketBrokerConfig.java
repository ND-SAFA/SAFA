package edu.nd.crc.safa.config;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.context.annotation.Configuration;
import org.springframework.messaging.simp.config.MessageBrokerRegistry;
import org.springframework.web.socket.config.annotation.EnableWebSocket;
import org.springframework.web.socket.config.annotation.EnableWebSocketMessageBroker;
import org.springframework.web.socket.config.annotation.StompEndpointRegistry;
import org.springframework.web.socket.config.annotation.WebSocketMessageBrokerConfigurer;
import org.springframework.web.socket.config.annotation.WebSocketTransportRegistration;

/**
 * Configures the general WebSocket configurations including:
 * - endpoint for initial connects to websockets
 * - setting message size
 * - setting the topic and individual message endpoints.
 */
@Configuration
@EnableWebSocket
@EnableWebSocketMessageBroker
public class WebSocketBrokerConfig implements WebSocketMessageBrokerConfigurer {

    public static final int messageSizeLimit = 50 * 1024 * 1024;
    private final Logger log = LoggerFactory.getLogger(WebSocketBrokerConfig.class);

    @Override
    public void configureWebSocketTransport(WebSocketTransportRegistration registration) {
        registration.setMessageSizeLimit(messageSizeLimit); // default : 64 * 1024
        registration.setSendBufferSizeLimit(messageSizeLimit); // default : 512 * 1024
    }

    @Override
    public void configureMessageBroker(MessageBrokerRegistry config) {
        config.enableSimpleBroker("/topic", "/queue");
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
