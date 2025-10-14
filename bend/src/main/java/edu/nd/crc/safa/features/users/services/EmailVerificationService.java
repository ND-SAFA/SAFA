package edu.nd.crc.safa.features.users.services;

import java.util.Date;

import edu.nd.crc.safa.authentication.TokenService;
import edu.nd.crc.safa.config.SecurityConstants;
import edu.nd.crc.safa.features.email.services.EmailService;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.db.EmailVerificationToken;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.repositories.EmailVerificationTokenRepository;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

/**
 * This service handles user email verification
 */
@Service
@AllArgsConstructor
public class EmailVerificationService {

    private final EmailVerificationTokenRepository tokenRepository;
    private final EmailService emailService;
    private final TokenService tokenService;
    private final SafaUserService safaUserService;

    /**
     * Generates an email verification token and sends an email to the user with
     * the link to verify their account.
     *
     * @param user The user to send the email to
     */
    public void sendVerificationEmail(SafaUser user) {
        tokenRepository.deleteByUser(user);

        Date expirationDate =
            new Date(System.currentTimeMillis() + SecurityConstants.ACCOUNT_CONFIRMATION_EXPIRATION_TIME);
        String token = tokenService.createTokenForUsername(user.getEmail(), expirationDate);
        EmailVerificationToken tokenDbo = new EmailVerificationToken(user, token, expirationDate);
        tokenRepository.save(tokenDbo);

        emailService.sendEmailVerification(user.getEmail(), token);
    }

    /**
     * Uses an email verification token to mark the associated account as verified.
     *
     * @param token The token
     * @throws SafaError If the token cannot be verified
     */
    public void verifyToken(String token) {
        EmailVerificationToken tokenObj = tokenRepository.findByToken(token)
            .orElseThrow(() -> new SafaError("Invalid token"));

        if (tokenObj.getExpirationDate().before(new Date())) {
            throw new SafaError("Expired token");
        }

        SafaUser user = tokenObj.getUser();
        safaUserService.setAccountVerification(user, true);
        tokenRepository.delete(tokenObj);
    }
}
