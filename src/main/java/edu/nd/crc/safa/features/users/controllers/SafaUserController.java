package edu.nd.crc.safa.features.users.controllers;

import java.io.IOException;
import java.util.Date;
import javax.validation.Valid;

import edu.nd.crc.safa.authentication.TokenService;
import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.config.SecurityConstants;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.email.EmailService;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.app.CreateAccountRequest;
import edu.nd.crc.safa.features.users.entities.app.PasswordChangeRequest;
import edu.nd.crc.safa.features.users.entities.app.PasswordForgottenRequest;
import edu.nd.crc.safa.features.users.entities.app.ResetPasswordRequestDTO;
import edu.nd.crc.safa.features.users.entities.app.UserIdentifierDTO;
import edu.nd.crc.safa.features.users.entities.app.UserPasswordDTO;
import edu.nd.crc.safa.features.users.entities.db.PasswordResetToken;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.repositories.PasswordResetTokenRepository;
import edu.nd.crc.safa.features.users.repositories.SafaUserRepository;
import edu.nd.crc.safa.features.users.services.SafaUserService;

import io.jsonwebtoken.Claims;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
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

    private static final Logger log = LoggerFactory.getLogger(SafaUserController.class);
    private final TokenService tokenService;
    private final PasswordEncoder passwordEncoder;
    private final SafaUserRepository safaUserRepository;
    private final SafaUserService safaUserService;
    private final EmailService emailService;
    private final PasswordResetTokenRepository passwordResetTokenRepository;
    @Value("${fend.base}")
    private String fendBase;
    @Value("${fend.reset-email-path}")
    private String fendPath;

    @Autowired
    public SafaUserController(ResourceBuilder resourceBuilder,
                              ServiceProvider serviceProvider,
                              EmailService emailService,
                              PasswordResetTokenRepository passwordResetTokenRepository) {
        super(resourceBuilder, serviceProvider);
        this.tokenService = serviceProvider.getTokenService();
        this.passwordEncoder = serviceProvider.getPasswordEncoder();
        this.safaUserRepository = serviceProvider.getSafaUserRepository();
        this.safaUserService = serviceProvider.getSafaUserService();
        this.emailService = emailService;
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
    public UserIdentifierDTO createNewUser(@RequestBody CreateAccountRequest newUser) throws IOException {
        // Step - Create user
        UserIdentifierDTO newUserIdentifierDTO = this.serviceProvider
            .getSafaUserService()
            .createUser(newUser.getEmail(), newUser.getPassword());
        return newUserIdentifierDTO;
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
        this.serviceProvider
            .getSafaUserService()
            .deleteUser(confirmationPassword);
    }

    /**
     * Sends email to authorized user email enabling them to create a new password.
     *
     * @param user The user to send the reset password email to.
     */
    @PutMapping(AppRoutes.Accounts.FORGOT_PASSWORD)
    public void forgotPassword(@Valid @RequestBody PasswordForgottenRequest user) {
        String username = user.getEmail();
        SafaUser retrievedUser = safaUserRepository.findByEmail(username)
            .orElseThrow(() -> new UsernameNotFoundException("Username does not exist: " + username));
        Date expirationDate = new Date(System.currentTimeMillis() + SecurityConstants.FORGOT_PASSWORD_EXPIRATION_TIME);
        String token = tokenService.createTokenForUsername(username, expirationDate);
        PasswordResetToken passwordResetToken = new PasswordResetToken(retrievedUser, token, expirationDate);

        try {
            emailService.send(
                "Requested password reset token",
                this.buildResetURL(token),
                user.getEmail()
            );
        } catch (Exception e) {
            log.error("Error occurred while trying to send email to {} " + e, user.getEmail());
            throw new SafaError("Could not send email");
        }

        this.passwordResetTokenRepository.save(passwordResetToken);
    }

    /**
     * Under construction. Sends email to reset password for
     *
     * @param passwordResetRequest Request containing token signed by user and their new password
     * @return {@link UserIdentifierDTO} The user identifier whose password was changed.
     */
    @PutMapping(AppRoutes.Accounts.RESET_PASSWORD)
    public UserIdentifierDTO resetPassword(@Valid @RequestBody ResetPasswordRequestDTO passwordResetRequest) {
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
        return new UserIdentifierDTO(retrievedUser);
    }

    /**
     * Updates the user's password to new one if their current password is validated.
     *
     * @param passwordChangeRequest Password change request containing current and new password.
     * @return {@link UserIdentifierDTO} The user entity whose password was set.
     */
    @PutMapping(AppRoutes.Accounts.CHANGE_PASSWORD)
    public UserIdentifierDTO changePassword(@Valid @RequestBody PasswordChangeRequest passwordChangeRequest) {
        SafaUser principal = safaUserService.getCurrentUser();

        if (passwordChangeRequest.getNewPassword().equals(passwordChangeRequest.getOldPassword())) {
            throw new SafaError("New password cannot be the same with the old one.");
        }

        if (!this.passwordEncoder.matches(passwordChangeRequest.getOldPassword(), principal.getPassword())) {
            throw new SafaError("Invalid old password");
        }

        principal.setPassword(passwordEncoder.encode(passwordChangeRequest.getNewPassword()));
        principal = this.safaUserRepository.save(principal);
        return new UserIdentifierDTO(principal);
    }

    @GetMapping(AppRoutes.Accounts.SELF)
    public UserIdentifierDTO retrieveCurrentUser() {
        return new UserIdentifierDTO(safaUserService.getCurrentUser());
    }

    private String buildResetURL(String token) {
        return String.format(fendBase + fendPath, token);
    }
}
