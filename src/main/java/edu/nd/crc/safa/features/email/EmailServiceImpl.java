package edu.nd.crc.safa.features.email;


import edu.nd.crc.safa.features.projects.entities.app.SafaError;

import jakarta.mail.internet.MimeMessage;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.messaging.MessagingException;

/**
 * Responsible for constructing and sending emails.
 */
public class EmailServiceImpl implements EmailService {
    private final JavaMailSender javaMailSender;

    @Autowired
    public EmailServiceImpl(JavaMailSender javaMailSender) {
        this.javaMailSender = javaMailSender;
    }

    @Override
    public void send(String subject, String messageContent, String recipient) throws Exception {
        throw new SafaError("Under construction.");
    }

    public MimeMessage createEmail(String subject, String messageContent, String recipient)
        throws MessagingException {
        throw new SafaError("Under construction.");
    }
}
