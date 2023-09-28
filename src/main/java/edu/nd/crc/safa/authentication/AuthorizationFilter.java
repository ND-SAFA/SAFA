package edu.nd.crc.safa.authentication;

import java.io.IOException;
import java.util.Arrays;
import java.util.Optional;

import edu.nd.crc.safa.config.SecurityConstants;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;

import io.jsonwebtoken.ExpiredJwtException;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.Cookie;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.web.authentication.www.BasicAuthenticationFilter;

/**
 * Intercepts request to resources and checks if a valid JWT is given to them.
 */
public class AuthorizationFilter extends BasicAuthenticationFilter {

    private final AuthorizationService authorizationService;


    public AuthorizationFilter(AuthenticationManager authManager,
                               AuthorizationService authorizationService) {
        super(authManager);
        this.authorizationService = authorizationService;
    }

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain chain) throws IOException, ServletException {
        try {
            if (request.getCookies() == null) {
                return;
            }

            Optional<String> token = Arrays.stream(request.getCookies())
                .filter(c -> c.getName().equals(SecurityConstants.JWT_COOKIE_NAME))
                .findFirst()
                .map(Cookie::getValue);

            if (token.isEmpty()) {
                return;
            }

            UsernamePasswordAuthenticationToken authenticationToken = authorizationService.authenticate(token.get());
            SecurityContextHolder.getContext().setAuthentication(authenticationToken);
        } catch (UsernameNotFoundException ignored) {
            // This happens if the user has a token for a deleted account. We have code that is supposed
            // to delete the cookie, so I don't know why it sticks around, but by catching the exception
            // we can at least keep the chain from dying
        } catch (ExpiredJwtException ignored) {
            // If your JWT expired, just move on and force the user to log in again
        } catch (SafaError e) {
            e.printStackTrace();
        } finally {
            chain.doFilter(request, response);
        }
    }
}
