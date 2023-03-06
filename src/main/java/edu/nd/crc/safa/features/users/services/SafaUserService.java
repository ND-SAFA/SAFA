package edu.nd.crc.safa.features.users.services;

import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.authentication.SafaUserDetails;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.app.UserIdentifierDTO;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.repositories.SafaUserRepository;

import lombok.AllArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContext;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

/**
 * Creates an implementation of UserDetailService and provides services for creating, authenticating,
 * and resetting users.
 */
@Service
@AllArgsConstructor
public class SafaUserService {

    private final Logger logger = LoggerFactory.getLogger(SafaUserService.class);

    private final PasswordEncoder passwordEncoder;
    private final SafaUserRepository safaUserRepository;

    // This exists solely so that it can be set to false during testing so that we can disable the check in that context
    private static boolean CHECK_USER_THREAD = true;

    /**
     * @return the current {@link SafaUser} logged in
     */
    public SafaUser getCurrentUser() {
        if (CHECK_USER_THREAD && !Thread.currentThread().getName().startsWith("https-jsse-nio-3000-exec")) {
            logger.warn("Attempt to get user information from a thread that does not appear to be a spring thread ("
                + Thread.currentThread().getName() + "). This is dangerous and should not be done.");
        }

        SecurityContext securityContext = SecurityContextHolder.getContext();
        Authentication authentication = securityContext.getAuthentication();

        return ((SafaUserDetails) authentication.getPrincipal()).getUser();
    }

    /**
     * Creates new user with given email and password.
     *
     * @param email    User's email. Must be unique.
     * @param password Account password
     * @return {@link UserIdentifierDTO} representing created user
     */
    public UserIdentifierDTO createUser(String email, String password) {
        String encodedPassword = this.passwordEncoder.encode(password);
        SafaUser safaUser = new SafaUser(email, encodedPassword);

        if (this.safaUserRepository.findByEmail(email).isPresent()) {
            throw new SafaError("Email already in use: " + email);
        }

        safaUser = this.safaUserRepository.save(safaUser);
        return new UserIdentifierDTO(safaUser);
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

        if (!confirmDelete) {
            throw new SafaError("Given password does not match our records");
        }

        this.safaUserRepository.delete(currentUser);
    }

    /**
     * Retrieves user with given email or throws error otherwise.
     *
     * @param email The email of the user to retrieve.
     * @return The user queried for
     */
    public SafaUser getUserByEmail(String email) {
        return this.safaUserRepository
            .findByEmail(email)
            .orElseThrow(() ->  new SafaError("No user exists with given email: %s.", email));
    }
}
