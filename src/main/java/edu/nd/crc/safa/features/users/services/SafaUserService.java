package edu.nd.crc.safa.features.users.services;

import static edu.nd.crc.safa.utilities.AssertUtils.assertPresent;

import java.util.Optional;
import java.util.UUID;
import java.util.function.Predicate;
import java.util.regex.Pattern;

import edu.nd.crc.safa.authentication.SafaUserDetails;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.PaymentTier;
import edu.nd.crc.safa.features.organizations.services.OrganizationService;
import edu.nd.crc.safa.features.permissions.services.PermissionService;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.app.SafaItemNotFoundError;
import edu.nd.crc.safa.features.users.entities.AccountCreatedEvent;
import edu.nd.crc.safa.features.users.entities.app.UserAppEntity;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.repositories.SafaUserRepository;

import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.context.ApplicationEventPublisher;
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

    // This exists solely so that it can be set to false during testing so that we can disable the check in that context
    private static boolean CHECK_USER_THREAD = true;
    private final Logger logger = LoggerFactory.getLogger(SafaUserService.class);
    private final PasswordEncoder passwordEncoder;
    private final SafaUserRepository safaUserRepository;
    private final OrganizationService organizationService;
    private final PermissionService permissionService;
    private final ApplicationEventPublisher applicationEventPublisher;

    private final Predicate<String> httpThreadPredicate = Pattern
        .compile("http(?:s-jsse)?-nio-\\S{1,20}-exec-\\d+")
        .asMatchPredicate();

    /**
     * @return the current {@link SafaUser} logged in
     */
    public SafaUser getCurrentUser() {
        if (CHECK_USER_THREAD && !httpThreadPredicate.test(Thread.currentThread().getName())) {
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
     * @return {@link SafaUser} representing created user
     */
    public SafaUser createUser(String email, String password) {
        String encodedPassword = this.passwordEncoder.encode(password);
        SafaUser safaUser = new SafaUser(email, encodedPassword);

        if (this.safaUserRepository.findByEmail(email).isPresent()) {
            throw new SafaError("Email already in use: " + email);
        }

        safaUser = this.safaUserRepository.save(safaUser);  // Save once so it gets an id

        Organization personalOrg = organizationService.createNewOrganization(
            new Organization(email, "", safaUser, PaymentTier.AS_NEEDED, true));
        safaUser.setPersonalOrgId(personalOrg.getId());
        safaUser.setDefaultOrgId(personalOrg.getId());
        safaUser = this.safaUserRepository.save(safaUser);  // Save again so it gets the org id

        applicationEventPublisher.publishEvent(new AccountCreatedEvent(this, safaUser));

        return safaUser;
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
     * @throws SafaItemNotFoundError If the user could not be found
     */
    public SafaUser getUserByEmail(String email) {
        return this.safaUserRepository
            .findByEmail(email)
            .orElseThrow(() -> new SafaItemNotFoundError("No user exists with given email: %s.", email));
    }

    /**
     * Get a user by their ID.
     *
     * @param userId The ID of the user
     * @return The user, if found
     * @throws SafaItemNotFoundError If the user could not be found
     */
    public SafaUser getUserById(UUID userId) {
        return safaUserRepository.findById(userId)
            .orElseThrow(() -> new SafaItemNotFoundError("No user exists with given ID: %s.", userId));
    }

    /**
     * Update a user's default org
     *
     * @param user            The user
     * @param newDefaultOrgId The new default org ID
     */
    public void updateDefaultOrg(SafaUser user, UUID newDefaultOrgId) {
        Optional<Organization> orgOpt = organizationService.getOrganizationOptionalById(newDefaultOrgId);
        assertPresent(orgOpt, "That organization does not exist.");

        user.setDefaultOrgId(newDefaultOrgId);
        safaUserRepository.save(user);
    }

    /**
     * Adds the superuser permission to the given user
     *
     * @param updatedUser The user to update
     */
    public void addSuperUser(SafaUser updatedUser) {
        updatedUser.setSuperuser(true);
        safaUserRepository.save(updatedUser);
    }

    /**
     * Removes the superuser permission from the given user
     *
     * @param updatedUser The user to update
     */
    public void removeSuperUser(SafaUser updatedUser) {
        updatedUser.setSuperuser(false);
        safaUserRepository.save(updatedUser);
    }

    /**
     * Mark an account as (un)verified.
     *
     * @param user The account
     * @param verified Whether the account is verified
     * @return The updated account
     */
    public SafaUser setAccountVerification(SafaUser user, boolean verified) {
        user.setVerified(verified);
        return safaUserRepository.save(user);
    }

    /**
     * Create an app entity for a user object
     *
     * @param user The object to convert
     * @return The converted app entity
     */
    public UserAppEntity toAppEntity(SafaUser user) {
        UserAppEntity entity = new UserAppEntity(user);
        if (permissionService.isSuperuser(user)) {
            entity.getAdmin().setActive(permissionService.isActiveSuperuser(user));
        }
        return entity;
    }
}
