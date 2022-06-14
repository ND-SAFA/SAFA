package edu.nd.crc.safa.server.authentication;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Objects;
import javax.servlet.FilterChain;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import edu.nd.crc.safa.config.SecurityConstants;
import edu.nd.crc.safa.server.entities.api.SafaError;

import io.jsonwebtoken.Claims;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.web.authentication.www.BasicAuthenticationFilter;

/**
 * Intercepts request to resources and checks if a valid JWT is given to them.
 */
public class AuthorizationFilter extends BasicAuthenticationFilter {

    private final TokenService tokenService;

    private final UserDetailsService userDetailsService;

    public AuthorizationFilter(AuthenticationManager authManager,
                               TokenService tokenService,
                               UserDetailsService userDetailsService) {
        super(authManager);
        this.tokenService = tokenService;
        this.userDetailsService = userDetailsService;
    }

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain chain) throws IOException, ServletException {
        String header = request.getHeader(SecurityConstants.AUTHORIZATION_HEADER);

        if (header == null) {
            chain.doFilter(request, response);
            return;
        }

        UsernamePasswordAuthenticationToken authenticationToken = null;
        try {
            authenticationToken = authenticate(request);
        } catch (SafaError e) {
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
    private UsernamePasswordAuthenticationToken authenticate(HttpServletRequest request) throws SafaError {
        String token = request.getHeader(SecurityConstants.AUTHORIZATION_HEADER);

        if (Objects.isNull(token)) {
            throw new SafaError("No token found.");
        }

        Claims userClaims = this.tokenService.getTokenClaims(token);
        String username = userClaims.getSubject();
        UserDetails userDetails = this.userDetailsService.loadUserByUsername(username);

        return new UsernamePasswordAuthenticationToken(userDetails, "", userDetails.getAuthorities());
    }
}
