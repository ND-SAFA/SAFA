package edu.nd.crc.safa.features.users.controllers;

import java.io.IOException;
import java.util.Date;
import java.util.List;
import javax.validation.Valid;

import edu.nd.crc.safa.authentication.TokenService;
import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.common.AuthorizationSetter;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.config.SecurityConstants;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.flatfiles.services.MultipartRequestService;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.app.CreateAccountRequest;
import edu.nd.crc.safa.features.users.entities.app.PasswordChangeRequest;
import edu.nd.crc.safa.features.users.entities.app.ResetPasswordRequestDTO;
import edu.nd.crc.safa.features.users.entities.app.UserIdentifierDTO;
import edu.nd.crc.safa.features.users.entities.app.UserPasswordDTO;
import edu.nd.crc.safa.features.users.entities.db.PasswordResetToken;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.repositories.SafaUserRepository;
import edu.nd.crc.safa.features.users.services.SafaUserService;

import io.jsonwebtoken.Claims;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

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

    @Autowired
    public SafaUserController(ResourceBuilder resourceBuilder,
                              ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
        this.tokenService = serviceProvider.getTokenService();
        this.passwordEncoder = serviceProvider.getPasswordEncoder();
        this.safaUserRepository = serviceProvider.getSafaUserRepository();
        this.safaUserService = serviceProvider.getSafaUserService();
    }

    /**
     * Creates new account with given email and password.
     * Error is thrown is email is already associated with another account.
     *
     * @param newUser User to create containing email and password.
     * @return Created user entity
     */
    @PostMapping(AppRoutes.Accounts.CREATE_ACCOUNT)
    public UserAppEntity createNewUser(@RequestBody SafaUser newUser) {
        return this.serviceProvider
            .getSafaUserService()
            .createUser(newUser.getEmail(), newUser.getPassword());
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

    @PutMapping(AppRoutes.Accounts.FORGOT_PASSWORD)
    // TODO: usually it's not a good idea to use entities as DTOs since Hibernate could create the given entity
    public void forgotPassword(@RequestBody SafaUser user) {
        String username = user.getEmail();
        SafaUser retrievedUser = safaUserRepository.findByEmail(username)
            .orElseThrow(() -> new UsernameNotFoundException("Username does not exist: " + username));

        Date expirationDate = new Date(System.currentTimeMillis() + SecurityConstants.FORGOT_PASSWORD_EXPIRATION_TIME);
        String token = tokenService.createTokenForUsername(username, expirationDate);
        PasswordResetToken passwordResetToken = new PasswordResetToken(retrievedUser, token, expirationDate);

        //TODO: Send email with reset token

    }

    @PutMapping(AppRoutes.Accounts.RESET_PASSWORD)
    public UserIdentifierDTO resetPassword(@RequestBody ResetPasswordRequestDTO passwordResetRequest) {
        // Step - Extract required information
        String resetToken = passwordResetRequest.getResetToken();
        String newPassword = passwordResetRequest.getNewPassword();

        // Step - Decode token and extract user
        Claims userClaims = this.tokenService.getTokenClaims(resetToken);
        String username = userClaims.getSubject();
        SafaUser retrievedUser = this.safaUserRepository.findByEmail(username)
            .orElseThrow(() -> new UsernameNotFoundException("Username does not exist:" + username));

        if (userClaims.getExpiration().before(new Date())) {
            throw new SafaError("Reset password token has expired.");
        }

        retrievedUser.setPassword(passwordEncoder.encode(newPassword));
        retrievedUser = this.safaUserRepository.save(retrievedUser);
        return new UserIdentifierDTO(retrievedUser);
    }

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
        return new UserAppEntity(principal);
    }
}
