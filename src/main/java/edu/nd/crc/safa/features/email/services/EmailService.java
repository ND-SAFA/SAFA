package edu.nd.crc.safa.features.email.services;

import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

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

    /**
     * Send an email indicating that a generation job completed.
     *
     * @param recipient The email of the recipient
     * @param projectVersion The project version the job was running on
     */
    void sendGenerationCompleted(String recipient, ProjectVersion projectVersion);

    /**
     * Send an email indicating that a generation job failed.
     *
     * @param recipient The email of the recipient
     * @param projectVersion The project version the job was running on
     */
    void sendGenerationFailed(String recipient, ProjectVersion projectVersion);
}
