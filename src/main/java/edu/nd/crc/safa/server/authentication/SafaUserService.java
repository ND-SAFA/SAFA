package edu.nd.crc.safa.server.authentication;

import edu.nd.crc.safa.server.accounts.SafaUser;
import edu.nd.crc.safa.server.repositories.projects.SafaUserRepository;

import lombok.AllArgsConstructor;
import org.springframework.context.annotation.Scope;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContext;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

/**
 * Creates an implementation of UserDetailService and provides services for creating, authenticating,
 * and resetting users.
 */
@Service
@Scope("singleton")
@AllArgsConstructor
public class SafaUserService implements UserDetailsService {

    private final SafaUserRepository safaUserRepository;

    /**
     * The implementation for UserDetailService that bridges Spring's default authentication and our
     * custom user entity class, SafaUser.
     */
    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        return new SafaUserDetails(this.getUserFromUsername(username));
    }

    public SafaUser getUserFromUsername(String username) {
        return safaUserRepository.findByEmail(username).orElseThrow(() -> new UsernameNotFoundException(username));
    }

    /**
     * @return the current {@link SafaUser} logged in
     */
    public SafaUser getCurrentUser() {
        SecurityContext securityContext = SecurityContextHolder.getContext();
        Authentication authentication = securityContext.getAuthentication();

        return ((SafaUserDetails) authentication.getPrincipal()).getUser();
    }
}
