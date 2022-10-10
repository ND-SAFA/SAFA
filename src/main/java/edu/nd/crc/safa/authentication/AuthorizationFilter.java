package edu.nd.crc.safa.authentication;

import java.io.IOException;
import java.util.Arrays;
import java.util.Optional;
import javax.servlet.FilterChain;
import javax.servlet.ServletException;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import edu.nd.crc.safa.config.SecurityConstants;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;

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
        if (request.getCookies() == null) {
            chain.doFilter(request, response);
            return;
        }

        Optional<String> token = Arrays.stream(request.getCookies())
            .filter(c -> c.getName().equals(SecurityConstants.JWT_COOKIE_NAME))
            .findFirst()
            .map(Cookie::getValue);

        if (token.isEmpty()) {
            chain.doFilter(request, response);
            return;
        }

        UsernamePasswordAuthenticationToken authenticationToken = null;

        try {
            authenticationToken = authenticate(token.get());
        } catch (SafaError e) {
            e.printStackTrace();
            return;
        }

        SecurityContextHolder.getContext().setAuthentication(authenticationToken);
        chain.doFilter(request, response);
    }

    /**
     * Parses the principal user within the JWT request token.
     *
     * @param token Request JWT
     * @return Successful authorization token if successful otherwise null.
     */
    private UsernamePasswordAuthenticationToken authenticate(String token) throws SafaError {
        Claims userClaims = this.tokenService.getTokenClaims(token);
        String username = userClaims.getSubject();
        UserDetails userDetails = this.userDetailsService.loadUserByUsername(username);

        return new UsernamePasswordAuthenticationToken(userDetails, "", userDetails.getAuthorities());
    }
}
