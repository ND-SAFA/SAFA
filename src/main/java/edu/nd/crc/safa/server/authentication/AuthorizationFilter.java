package edu.nd.crc.safa.server.authentication;

import static edu.nd.crc.safa.config.SecurityConstants.HEADER_NAME;
import static edu.nd.crc.safa.config.SecurityConstants.KEY;

import java.io.IOException;
import java.util.ArrayList;
import javax.servlet.FilterChain;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import edu.nd.crc.safa.server.entities.api.ServerError;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.web.authentication.www.BasicAuthenticationFilter;

/**
 * Intercepts request to resources and checks if a valid JWT is given to them.
 */
public class AuthorizationFilter extends BasicAuthenticationFilter {

    public AuthorizationFilter(AuthenticationManager authManager) {
        super(authManager);
    }

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain chain) throws IOException, ServletException {
        String header = request.getHeader(HEADER_NAME);

        if (header == null) {
            chain.doFilter(request, response);
            return;
        }

        UsernamePasswordAuthenticationToken authentication = null;
        try {
            authentication = authenticate(request);
        } catch (ServerError e) {
            e.printStackTrace();
            return;
        }
        SecurityContextHolder.getContext().setAuthentication(authentication);
        chain.doFilter(request, response);
    }

    /**
     * Retrieves JWT token from request header and parses the principal user within it.
     *
     * @param request An incoming http request.
     * @return Successful authorization token if successful otherwise null.
     */
    private UsernamePasswordAuthenticationToken authenticate(HttpServletRequest request) throws ServerError {
        String token = request.getHeader(HEADER_NAME);
        if (token != null) {
            //TODO: replace these deprecated methods
            Claims user = Jwts.parser()
                .setSigningKey(Keys.hmacShaKeyFor(KEY.getBytes()))
                .parseClaimsJws(token)
                .getBody();

            if (user != null) {
                return new UsernamePasswordAuthenticationToken(user, null, new ArrayList<>());
            } else {
                return null;
            }

        }
        throw new ServerError("No token found.");
    }
}
