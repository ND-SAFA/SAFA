package edu.nd.crc.safa.server.services;

import javax.mail.MessagingException;
import javax.mail.internet.MimeMessage;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.stereotype.Service;

/**
 * Responsible for constructing and sending emails.
 */
@Service
public class MailService {
    private final JavaMailSender javaMailSender;

    @Autowired
    public MailService(JavaMailSender javaMailSender) {
        this.javaMailSender = javaMailSender;
    }

    public void createAndSendEmail(String subject, String messageContent, String recipient) throws MessagingException {
        sendMessage(createEmail(subject, messageContent, recipient));
    }

    public MimeMessage createEmail(String subject, String messageContent, String recipient)
        throws MessagingException {
        MimeMessage mimeMessage = javaMailSender.createMimeMessage();
        MimeMessageHelper messageHelper = new MimeMessageHelper(mimeMessage);
        messageHelper.setTo(recipient);
        messageHelper.setSubject(subject);
        messageHelper.setText(messageContent, true);
        return mimeMessage;
    }

    public void sendMessage(MimeMessage mimeMessage) {
        javaMailSender.send(mimeMessage);
    }
}
