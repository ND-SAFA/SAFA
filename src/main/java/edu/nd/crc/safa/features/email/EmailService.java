package edu.nd.crc.safa.features.email;

/**
 * Interface defining the send-email operation
 */
public interface EmailService {

    void send(String subject, String messageContent, String recipient) throws Exception;
}
