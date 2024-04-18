package edu.nd.crc.safa.features.email.services;

import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

/**
 * Interface defining the send-email operation.
 */
public interface EmailService {

    /**
     * Send a password reset token email.
     *
     * @param recipient The email of the recipient
     * @param resetAccount The email of the account we're resetting (usually but not always the same as recipient)
     * @param token The password reset token
     */
    void sendPasswordReset(String recipient, String resetAccount, String token);

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
     * @param jobEntity The job that ran the generation. May be null
     */
    void sendGenerationCompleted(String recipient, ProjectVersion projectVersion, JobDbEntity jobEntity);

    /**
     * Send an email indicating that a generation job failed.
     *
     * @param recipient The email of the recipient
     * @param projectVersion The project version the job was running on
     * @param jobEntity The job that ran the generation. May be null
     */
    void sendGenerationFailed(String recipient, ProjectVersion projectVersion, JobDbEntity jobEntity);

    /**
     * Send an email indicating that a generation job finished.
     *
     * @param recipient The email of the recipient
     * @param projectVersion The project version the job was running on
     * @param jobEntity The job that ran the generation. May be null
     * @param success Whether the generation finished successfully
     */
    default void sendGenerationFinished(String recipient, ProjectVersion projectVersion,
                                        JobDbEntity jobEntity, boolean success) {
        if (success) {
            sendGenerationCompleted(recipient, projectVersion, jobEntity);
        } else {
            sendGenerationFailed(recipient, projectVersion, jobEntity);
        }
    }
}
