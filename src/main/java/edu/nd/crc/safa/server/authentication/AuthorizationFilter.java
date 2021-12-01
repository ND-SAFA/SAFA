package edu.nd.crc.safa.server.authentication;

import static edu.nd.crc.safa.config.SecurityConstants.AUTHORIZATION_HEADER;

import java.io.IOException;
import java.util.ArrayList;
import javax.servlet.FilterChain;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import edu.nd.crc.safa.server.entities.api.ServerError;

import io.jsonwebtoken.Claims;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.web.authentication.www.BasicAuthenticationFilter;

/**
 * Intercepts request to resources and checks if a valid JWT is given to them.
 */
public class AuthorizationFilter extends BasicAuthenticationFilter {

    private final TokenService tokenService;

    public AuthorizationFilter(AuthenticationManager authManager,
                               TokenService tokenService) {
        super(authManager);
        this.tokenService = tokenService;
    }

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain chain) throws IOException, ServletException {
        String header = request.getHeader(AUTHORIZATION_HEADER);

        if (header == null) {
            chain.doFilter(request, response);
            return;
        }

        UsernamePasswordAuthenticationToken authenticationToken = null;
        try {
            authenticationToken = authenticate(request);
        } catch (ServerError e) {
            e.printStackTrace();
            return;
        }
        SecurityContextHolder.getContext().setAuthentication(authenticationToken);
        chain.doFilter(request, response);
    }

    /**
     * Retrieves JWT token from request header and parses the principal user within it.
     *
     * @param request An incoming http request.
     * @return Successful authorization token if successful otherwise null.
     */
    private UsernamePasswordAuthenticationToken authenticate(HttpServletRequest request) throws ServerError {
        String token = request.getHeader(AUTHORIZATION_HEADER);
        if (token != null) {
            Claims userClaims = this.tokenService.getTokenClaims(token);
            return new UsernamePasswordAuthenticationToken(userClaims, null, new ArrayList<>());
        }
        throw new ServerError("No token found.");
    }
}
