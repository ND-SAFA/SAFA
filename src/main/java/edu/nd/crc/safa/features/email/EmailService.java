package edu.nd.crc.safa.features.email;

/**
 * Interface defining the send-email operation
 */
public interface EmailService {

    void sendPasswordReset(String recipient, String token);
}
