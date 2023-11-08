package edu.nd.crc.safa.features.users.controllers;

import java.util.Date;
import java.util.UUID;

import edu.nd.crc.safa.authentication.TokenService;
import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.config.SecurityConstants;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.email.EmailService;
import edu.nd.crc.safa.features.permissions.MissingPermissionException;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.app.CreateAccountRequest;
import edu.nd.crc.safa.features.users.entities.app.PasswordChangeRequest;
import edu.nd.crc.safa.features.users.entities.app.PasswordForgottenRequest;
import edu.nd.crc.safa.features.users.entities.app.ResetPasswordRequestDTO;
import edu.nd.crc.safa.features.users.entities.app.UserAppEntity;
import edu.nd.crc.safa.features.users.entities.app.UserPasswordDTO;
import edu.nd.crc.safa.features.users.entities.db.PasswordResetToken;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.repositories.PasswordResetTokenRepository;
import edu.nd.crc.safa.features.users.repositories.SafaUserRepository;
import edu.nd.crc.safa.features.users.services.EmailVerificationService;
import edu.nd.crc.safa.features.users.services.SafaUserService;

import io.jsonwebtoken.Claims;
import jakarta.transaction.Transactional;
import jakarta.validation.Valid;
import lombok.AllArgsConstructor;
import lombok.Data;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

/**
 * Controller containing endpoints for:
 * 1. Creating a new account
 * 2. Resetting user password (TODO)
 * 3. Confirming user account (TODO)
 * Note, logging into system is handled by spring boot default configuration at /login.
 */
@RestController
public class SafaUserController extends BaseController {

    private final TokenService tokenService;
    private final PasswordEncoder passwordEncoder;
    private final SafaUserRepository safaUserRepository;
    private final SafaUserService safaUserService;
    private final EmailService emailService;
    private final EmailVerificationService emailVerificationService;
    private final PasswordResetTokenRepository passwordResetTokenRepository;

    @Autowired
    public SafaUserController(ResourceBuilder resourceBuilder,
                              ServiceProvider serviceProvider,
                              EmailService emailService,
                              EmailVerificationService emailVerificationService,
                              PasswordResetTokenRepository passwordResetTokenRepository) {
        super(resourceBuilder, serviceProvider);
        this.tokenService = serviceProvider.getTokenService();
        this.passwordEncoder = serviceProvider.getPasswordEncoder();
        this.safaUserRepository = serviceProvider.getSafaUserRepository();
        this.safaUserService = serviceProvider.getSafaUserService();
        this.emailService = emailService;
        this.emailVerificationService = emailVerificationService;
        this.passwordResetTokenRepository = passwordResetTokenRepository;
    }

    /**
     * Creates new account with given email and password.
     * Error is thrown is email is already associated with another account.
     *
     * @param newUser User to create containing email and password.
     * @return Created user entity
     */
    @PostMapping(AppRoutes.Accounts.CREATE_ACCOUNT)
    public UserAppEntity createNewUser(@RequestBody CreateAccountRequest newUser) {
        // Step - Create user
        SafaUser createdAccount = getServiceProvider()
            .getSafaUserService()
            .createUser(newUser.getEmail(), newUser.getPassword());

        emailVerificationService.sendVerificationEmail(createdAccount);

        return new UserAppEntity(createdAccount);
    }

    /**
     * <p>Creates new account with given email and password.
     * Error is thrown is email is already associated with another account.</p>
     *
     * <p>The created account will be automatically verified and will not send
     * a verification email.</p>
     *
     * <p>This action can only be done by a superuser</p>
     *
     * @param newUser User to create containing email and password.
     * @return Created user entity
     */
    @PostMapping(AppRoutes.Accounts.CREATE_VERIFIED_ACCOUNT)
    public UserAppEntity createNewVerifiedUser(@RequestBody CreateAccountRequest newUser) {
        SafaUser currentUser = getCurrentUser();
        if (!currentUser.isSuperuser()) {
            throw new MissingPermissionException(() -> "safa.create_verified_account");
        }

        SafaUser createdAccount = safaUserService.createUser(newUser.getEmail(), newUser.getPassword());
        createdAccount = safaUserService.setAccountVerification(createdAccount, true);
        return new UserAppEntity(createdAccount);
    }

    /**
     * Verify a user's email from an email verification token
     *
     * @param token The email verification token
     */
    @PostMapping(AppRoutes.Accounts.VERIFY_ACCOUNT)
    public void verifyAccount(@RequestBody AccountVerificationDTO token) {
        emailVerificationService.verifyToken(token.getToken());
    }

    /**
     * Deletes account of authenticated user after confirming that given
     * password matches that of database.
     *
     * @param userPasswordDTO Authenticated user's password.
     */
    @PostMapping(AppRoutes.Accounts.DELETE_ACCOUNT)
    public void deleteAccount(@RequestBody UserPasswordDTO userPasswordDTO) {
        String confirmationPassword = userPasswordDTO.getPassword();
        if (confirmationPassword == null) {
            throw new SafaError("Received empty confirmation password.");
        }
        getServiceProvider()
            .getSafaUserService()
            .deleteUser(confirmationPassword);
    }

    /**
     * Sends email to authorized user email enabling them to create a new password.
     *
     * @param user The user to send the reset password email to.
     */
    @Transactional
    @PutMapping(AppRoutes.Accounts.FORGOT_PASSWORD)
    public void forgotPassword(@Valid @RequestBody PasswordForgottenRequest user) {
        String username = user.getEmail();
        SafaUser retrievedUser = safaUserRepository.findByEmail(username)
            .orElseThrow(() -> new UsernameNotFoundException("Username does not exist: " + username));
        Date expirationDate = new Date(System.currentTimeMillis() + SecurityConstants.FORGOT_PASSWORD_EXPIRATION_TIME);
        String token = tokenService.createTokenForUsername(username, expirationDate);
        PasswordResetToken passwordResetToken = new PasswordResetToken(retrievedUser, token, expirationDate);

        emailService.sendPasswordReset(user.getEmail(), token);

        // Just in case the user had a previous forget token they never clicked on
        this.passwordResetTokenRepository.deleteByUser(retrievedUser);
        this.passwordResetTokenRepository.flush();

        this.passwordResetTokenRepository.save(passwordResetToken);
    }

    /**
     * Under construction. Sends email to reset password for
     *
     * @param passwordResetRequest Request containing token signed by user and their new password
     * @return {@link UserAppEntity} The user identifier whose password was changed.
     */
    @PutMapping(AppRoutes.Accounts.RESET_PASSWORD)
    public UserAppEntity resetPassword(@Valid @RequestBody ResetPasswordRequestDTO passwordResetRequest) {
        // Step - Extract required information
        String resetToken = passwordResetRequest.getResetToken();
        String newPassword = passwordResetRequest.getNewPassword();

        // Step - check the reset token was issued by us
        PasswordResetToken passwordResetToken = passwordResetTokenRepository.findByToken(resetToken)
            .orElseThrow(() -> new SafaError("Illegal expiration token"));

        resetToken = passwordResetToken.getToken();

        // Step - Decode token and extract user
        Claims userClaims = this.tokenService.getTokenClaims(resetToken);
        String username = userClaims.getSubject();
        SafaUser retrievedUser = this.safaUserRepository.findByEmail(username)
            .orElseThrow(() -> new UsernameNotFoundException("Username does not exist:" + username));

        // Step - Check the token has no expired
        if (userClaims.getExpiration().before(new Date())) {
            throw new SafaError("Reset password token has expired.");
        }

        retrievedUser.setPassword(passwordEncoder.encode(newPassword));
        retrievedUser = this.safaUserRepository.save(retrievedUser);
        this.passwordResetTokenRepository.delete(passwordResetToken);
        return new UserAppEntity(retrievedUser);
    }

    /**
     * Updates the user's password to new one if their current password is validated.
     *
     * @param passwordChangeRequest Password change request containing current and new password.
     * @return {@link UserAppEntity} The user entity whose password was set.
     */
    @PutMapping(AppRoutes.Accounts.CHANGE_PASSWORD)
    public UserAppEntity changePassword(@Valid @RequestBody PasswordChangeRequest passwordChangeRequest) {
        SafaUser principal = safaUserService.getCurrentUser();

        if (passwordChangeRequest.getNewPassword().equals(passwordChangeRequest.getOldPassword())) {
            throw new SafaError("New password cannot be the same with the old one.");
        }

        if (!this.passwordEncoder.matches(passwordChangeRequest.getOldPassword(), principal.getPassword())) {
            throw new SafaError("Invalid old password");
        }

        principal.setPassword(passwordEncoder.encode(passwordChangeRequest.getNewPassword()));
        principal = this.safaUserRepository.save(principal);
        return new UserAppEntity(principal);
    }

    @GetMapping(AppRoutes.Accounts.SELF)
    public UserAppEntity retrieveCurrentUser() {
        return new UserAppEntity(safaUserService.getCurrentUser());
    }

    @PutMapping(AppRoutes.Accounts.DEFAULT_ORG)
    public void updateDefaultOrg(@RequestBody DefaultOrgDTO newOrgDto) {
        SafaUser currentUser = getCurrentUser();
        safaUserService.updateDefaultOrg(currentUser, newOrgDto.defaultOrgId);
    }

    @Data
    public static class DefaultOrgDTO {
        private UUID defaultOrgId;
    }

    @Data
    @AllArgsConstructor
    public static class AccountVerificationDTO {
        private String token;
    }
}
