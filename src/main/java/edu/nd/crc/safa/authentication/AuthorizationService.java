package edu.nd.crc.safa.authentication;

import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.app.UserAppEntity;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.services.SafaUserService;

import io.jsonwebtoken.Claims;
import lombok.AccessLevel;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import org.springframework.context.annotation.Lazy;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.stereotype.Service;

@RequiredArgsConstructor
@Service
public class AuthorizationService {
    private final TokenService tokenService;
    private final UserDetailsService userDetailsService;

    @Setter(value = AccessLevel.PRIVATE, onMethod = @__({@Lazy}))
    private SafaUserService safaUserService;

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

    public UserAppEntity getUser(String token) throws SafaError {
        Claims userClaims = this.tokenService.getTokenClaims(token);
        String username = userClaims.getSubject();
        SafaUser safaUser = safaUserService.getUserByEmail(username);
        return safaUserService.toAppEntity(safaUser);
    }
}
