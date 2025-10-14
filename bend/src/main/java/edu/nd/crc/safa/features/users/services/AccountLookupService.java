package edu.nd.crc.safa.features.users.services;

import edu.nd.crc.safa.authentication.SafaUserDetails;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.repositories.SafaUserRepository;

import lombok.AllArgsConstructor;
import org.springframework.context.annotation.Scope;
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
public class AccountLookupService implements UserDetailsService {

    private final SafaUserRepository safaUserRepository;

    /**
     * The implementation for UserDetailService that bridges Spring's default authentication and our
     * custom user entity class, {@link SafaUser}.
     */
    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        return new SafaUserDetails(this.getUserFromUsername(username));
    }

    public SafaUser getUserFromUsername(String username) {
        return safaUserRepository.findByEmail(username).orElseThrow(() -> new UsernameNotFoundException(username));
    }
}
