package edu.nd.crc.safa.authentication;

import edu.nd.crc.safa.features.projects.entities.app.SafaError;

import io.jsonwebtoken.Claims;
import lombok.AllArgsConstructor;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.stereotype.Service;

@AllArgsConstructor
@Service
public class AuthorizationService {
    private final TokenService tokenService;
    private final UserDetailsService userDetailsService;

    /**
     * Parses the principal user within the JWT request token.
     *
     * @param token Request JWT
     * @return Successful authorization token if successful otherwise null.
     */
    public UsernamePasswordAuthenticationToken authenticate(String token) throws SafaError {
        Claims userClaims = this.tokenService.getTokenClaims(token);
        String username = userClaims.getSubject();
        UserDetails userDetails = this.userDetailsService.loadUserByUsername(username);

        return new UsernamePasswordAuthenticationToken(userDetails, "", userDetails.getAuthorities());
    }
}
