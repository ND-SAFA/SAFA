package edu.nd.crc.safa.server.authentication;

import edu.nd.crc.safa.server.entities.db.SafaUser;
import edu.nd.crc.safa.server.repositories.SafaUserRepository;

import io.jsonwebtoken.Claims;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;
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
public class SafaUserService implements UserDetailsService {

    SafaUserRepository safaUserRepository;

    @Autowired
    public SafaUserService(SafaUserRepository safaUserRepository
    ) {
        this.safaUserRepository = safaUserRepository;
    }

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
        final SafaUser user = safaUserRepository.findByEmail(userName);
        if (user == null) {
            throw new UsernameNotFoundException(userName);
        }
        return user;
    }

    public SafaUser getUserFromAuthentication(Authentication user) {
        String userName = ((Claims) user.getPrincipal()).getSubject();
        return this.getUserFromUsername(userName);
    }
}
