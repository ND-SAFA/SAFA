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
    public void forgotPassword(@RequestBody SafaUser user) {
        String username = user.getEmail();
        Optional<SafaUser> retrievedUserOptional = this.safaUserRepository.findByEmail(username);
        if (retrievedUserOptional.isPresent()) {
            SafaUser retrievedUser = retrievedUserOptional.get();
            String token = this.tokenService.createTokenForUsername(username,
                SecurityConstants.FORGOT_PASSWORD_EXPIRATION_TIME);
            PasswordResetToken passwordResetToken = new PasswordResetToken(retrievedUser,
                token);

            //TODO: Send email with reset token
        } else {
            throw new UsernameNotFoundException("Username does not exist:" + username);
        }
    }

    @PutMapping(AppRoutes.Accounts.resetPassword)
    public UserAppEntity resetPassword(@RequestBody ResetPasswordAppEntity passwordResetToken) {
        // Step - Extract required information
        String resetToken = passwordResetToken.getResetToken();
        String newPassword = passwordResetToken.getNewPassword();

        // Step - Decode token and extract user
        Claims userClaims = this.tokenService.getTokenClaims(resetToken);
        String username = userClaims.getSubject();
        Optional<SafaUser> retrievedUserOptional = this.safaUserRepository.findByEmail(username);

        // TODO: Refactor this comparison to user non-deprecated methods
        int dateComparison = userClaims.getExpiration().compareTo(new Date(LocalDateTime.now().toString()));
        if (dateComparison < 1) {
            throw new SafaError("Reset password token has expired.");
        }

        // Step - Save new password
        if (retrievedUserOptional.isPresent()) {
            SafaUser retrievedUser = retrievedUserOptional.get();
            retrievedUser.setPassword(passwordEncoder.encode(newPassword));
            this.safaUserRepository.save(retrievedUser);
            return new UserAppEntity(retrievedUser);
        } else {
            throw new UsernameNotFoundException("Username does not exist:" + username);
        }
    }
}
