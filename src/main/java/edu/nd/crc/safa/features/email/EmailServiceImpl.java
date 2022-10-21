package edu.nd.crc.safa.features.email;

import javax.mail.MessagingException;
import javax.mail.internet.MimeMessage;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.stereotype.Service;

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
