package edu.nd.crc.safa.features.email;

/**
 * Interface defining the send-email operation.
 */
public interface EmailService {

    /**
     * Send a password reset token email.
     *
     * @param recipient The email of the recipient
     * @param token The password reset token
     */
    void sendPasswordReset(String recipient, String token);

    /**
     * Send an email verification email.
     *
     * @param recipient The email of the recipient
     * @param token The email verification token
     */
    void sendEmailVerification(String recipient, String token);
}
