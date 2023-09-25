package edu.nd.crc.safa.config;

import java.security.Principal;
import java.util.Map;

import edu.nd.crc.safa.authentication.AuthorizationService;

import org.springframework.http.server.ServerHttpRequest;
import org.springframework.http.server.ServerHttpResponse;
import org.springframework.messaging.simp.SimpMessageHeaderAccessor;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.web.socket.WebSocketHandler;
import org.springframework.web.socket.server.support.HttpSessionHandshakeInterceptor;


public class WebSocketHandshakeInterceptor extends HttpSessionHandshakeInterceptor {
    private AuthorizationService authorizationService;

    public WebSocketHandshakeInterceptor(AuthorizationService authorizationService) {
        this.authorizationService = authorizationService;
    }

    @Override
    public boolean beforeHandshake(ServerHttpRequest request,
                                   ServerHttpResponse response,
                                   WebSocketHandler wsHandler,
                                   Map<String, Object> attributes) throws Exception {
        // Extract and validate JWT from the request headers
        // Set user information in the WebSocket session attributes if JWT is valid
        Principal principal = request.getPrincipal();
        String authorizationToken = request.getHeaders().get("SAFA-TOKEN").get(0);
        UsernamePasswordAuthenticationToken authorization = authorizationService.authenticate(authorizationToken);
        attributes.put(SimpMessageHeaderAccessor.USER_HEADER, authorization);
        setCopyAllAttributes(true);
        return super.beforeHandshake(request, response, wsHandler, attributes);
    }
}
