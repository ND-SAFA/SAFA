package edu.nd.crc.safa.authentication;

import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.repositories.SafaUserRepository;

import lombok.AllArgsConstructor;
import org.springframework.context.annotation.Scope;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContext;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.password.PasswordEncoder;
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
    private final PasswordEncoder passwordEncoder;

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

    /**
     * @return the current {@link SafaUser} logged in
     */
    public SafaUser getCurrentUser() {
        SecurityContext securityContext = SecurityContextHolder.getContext();
        Authentication authentication = securityContext.getAuthentication();

        return ((SafaUserDetails) authentication.getPrincipal()).getUser();
    }

    /**
     * Deletes authenticated {@link SafaUser} if given password matches stored records
     * once encoded. Otherwise, error is thrown.
     *
     * @param password The password to confirm account deletion.
     */
    public void deleteUser(@NotNull String password) {
        SafaUser currentUser = this.getCurrentUser();
        String encodedPassword = currentUser.getPassword();
        boolean confirmDelete = this.passwordEncoder.matches(password, encodedPassword);
        if (confirmDelete) {
            this.safaUserRepository.delete(currentUser);
        } else {
            throw new SafaError("Given password does not match our records");
        }
    }
}
