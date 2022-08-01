package edu.nd.crc.safa.server.accounts;

import java.time.LocalDateTime;
import java.util.Date;
import java.util.Optional;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.config.SecurityConstants;
import edu.nd.crc.safa.server.authentication.TokenService;
import edu.nd.crc.safa.server.controllers.BaseController;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.repositories.projects.SafaUserRepository;

import io.jsonwebtoken.Claims;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.password.PasswordEncoder;
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

    private final SafaUserRepository safaUserRepository;
    private final PasswordEncoder passwordEncoder;
    private final TokenService tokenService;

    @Autowired
    public SafaUserController(ResourceBuilder resourceBuilder,
                              SafaUserRepository safaUserRepository,
                              PasswordEncoder passwordEncoder,
                              TokenService tokenService) {
        super(resourceBuilder);
        this.safaUserRepository = safaUserRepository;
        this.passwordEncoder = passwordEncoder;
        this.tokenService = tokenService;
    }

    @PostMapping(AppRoutes.Accounts.createNewUser)
    public UserAppEntity createNewUser(@RequestBody SafaUser newUser) {
        newUser.setPassword(this.passwordEncoder.encode(newUser.getPassword()));
        this.safaUserRepository.save(newUser);
        return new UserAppEntity(newUser);
    }

    @PutMapping(AppRoutes.Accounts.forgotPassword)
    // TODO: usually it's not a idea to use entities as DTOs
    public void forgotPassword(@RequestBody SafaUser user) {
        String username = user.getEmail();
        SafaUser retrievedUser = this.safaUserRepository.findByEmail(username)
                .orElseThrow(() -> new UsernameNotFoundException("Username does not exist: " + username));

        Date expirationDate = new Date(System.currentTimeMillis() + SecurityConstants.FORGOT_PASSWORD_EXPIRATION_TIME);
        String token = this.tokenService.createTokenForUsername(username, expirationDate);
        PasswordResetToken passwordResetToken = new PasswordResetToken(retrievedUser, token, expirationDate);

        //TODO: Send email with reset token

    }

    @PutMapping(AppRoutes.Accounts.resetPassword)
    public UserAppEntity resetPassword(@RequestBody ResetPasswordAppEntity passwordResetToken) {
        // Step - Extract required information
        String resetToken = passwordResetToken.getResetToken();
        String newPassword = passwordResetToken.getNewPassword();

        // Step - Decode token and extract user
        Claims userClaims = this.tokenService.getTokenClaims(resetToken);
        String username = userClaims.getSubject();
        SafaUser retrievedUser = this.safaUserRepository.findByEmail(username)
                .orElseThrow(() -> new UsernameNotFoundException("Username does not exist:" + username));

        if (userClaims.getExpiration().before(new Date())) {
            throw new SafaError("Reset password token has expired.");
        }

        retrievedUser.setPassword(passwordEncoder.encode(newPassword));
        this.safaUserRepository.save(retrievedUser);
        return new UserAppEntity(retrievedUser);
    }
}
