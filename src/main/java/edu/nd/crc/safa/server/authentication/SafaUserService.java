package edu.nd.crc.safa.server.authentication;

import java.util.Optional;

import edu.nd.crc.safa.server.entities.db.SafaUser;
import edu.nd.crc.safa.server.repositories.projects.SafaUserRepository;

import io.jsonwebtoken.Claims;
import lombok.AllArgsConstructor;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

/**
 * Creates an implementation of UserDetailService and provides services for creating, authenticating,
 * and resetting users.
 */
@Service
@AllArgsConstructor
public class SafaUserService implements UserDetailsService {

    private final SafaUserRepository safaUserRepository;

    /**
     * The implementation for UserDetailService that bridges Spring's default authentication and our
     * custom user entity class, SafaUser.
     */
    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        final SafaUser customer = getUserFromUsername(username);
        return User
            .withUsername(customer.getEmail())
            .password(customer.getPassword())
            .authorities("USER") // TODO: Replace with custom roles here
            .build();
    }

    public SafaUser getUserFromUsername(String userName) {
        final Optional<SafaUser> userQuery = safaUserRepository.findByEmail(userName);
        if (userQuery.isEmpty()) {
            throw new UsernameNotFoundException(userName);
        }
        return userQuery.get();
    }

    public SafaUser getCurrentUser() {
        Authentication user = SecurityContextHolder.getContext().getAuthentication();
        String userName = ((Claims) user.getPrincipal()).getSubject();
        return this.getUserFromUsername(userName);
    }
}
