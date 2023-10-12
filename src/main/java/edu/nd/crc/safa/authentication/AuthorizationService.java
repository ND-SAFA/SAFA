package edu.nd.crc.safa.authentication;

import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.app.UserAppEntity;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.repositories.SafaUserRepository;

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
    private final SafaUserRepository safaUserRepository;

    /**
     * Parses the principal user within the JWT request token.
     *
     * @param token Request JWT
     * @return Successful authorization token if successful otherwise null.
     */
    public UsernamePasswordAuthenticationToken authenticate(String token) throws SafaError {
        System.out.println("starting authorization...");
        Claims userClaims = this.tokenService.getTokenClaims(token);
        System.out.println("user claims..." + userClaims);
        String username = userClaims.getSubject();
        UserDetails userDetails = this.userDetailsService.loadUserByUsername(username);
        System.out.println("user details..." + userDetails);
        return new UsernamePasswordAuthenticationToken(userDetails, "", userDetails.getAuthorities());
    }

    public UserAppEntity getUser(String token) throws SafaError {
        Claims userClaims = this.tokenService.getTokenClaims(token);
        String username = userClaims.getSubject();
        SafaUser safaUser = safaUserRepository.findByEmail(username).orElseThrow();
        return new UserAppEntity(safaUser);
    }
}
