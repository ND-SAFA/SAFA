package edu.nd.crc.safa.features.users.services;

import java.util.Optional;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.authentication.SafaUserDetails;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.app.UserIdentifierDTO;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.repositories.SafaUserRepository;

import lombok.AllArgsConstructor;
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

    private final PasswordEncoder passwordEncoder;
    private final SafaUserRepository safaUserRepository;

    /**
     * @return the current {@link SafaUser} logged in
     */
    public SafaUser getCurrentUser() {
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
        this.safaUserRepository.save(safaUser);
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
        if (confirmDelete) {
            this.safaUserRepository.delete(currentUser);
        } else {
            throw new SafaError("Given password does not match our records");
        }
    }

    /**
     * Retrieves user with given email or throws error otherwise.
     *
     * @param email The email of the user to retrieve.
     * @return The user queried for
     */
    public SafaUser getUserByEmail(String email) {
        Optional<SafaUser> newMemberQuery = this.safaUserRepository.findByEmail(email);
        if (newMemberQuery.isEmpty()) {
            throw new SafaError("No user exists with given email: %s.", email);
        }
        return newMemberQuery.get();
    }
}
