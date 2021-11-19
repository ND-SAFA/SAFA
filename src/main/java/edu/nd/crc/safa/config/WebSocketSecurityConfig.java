package edu.nd.crc.safa.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.messaging.MessageSecurityMetadataSourceRegistry;
import org.springframework.security.config.annotation.web.socket.AbstractSecurityWebSocketMessageBrokerConfigurer;

/**
 * Configures the security protocols surrounding websocket messages.
 * TODO: Replace empty policy with a token-based one.
 */
@Configuration
public class WebSocketSecurityConfig extends AbstractSecurityWebSocketMessageBrokerConfigurer {

    @Override
    protected void configureInbound(MessageSecurityMetadataSourceRegistry messages) {
        messages
            .anyMessage()
            .permitAll();
    }

    @Override
    protected boolean sameOriginDisabled() {
        return true;
    }
}
