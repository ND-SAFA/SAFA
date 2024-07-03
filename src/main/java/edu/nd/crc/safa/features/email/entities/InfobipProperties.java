package edu.nd.crc.safa.features.email.entities;

import java.util.Map;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "email.infobip")
@Data
public class InfobipProperties {
    private final String endpoint;
    private final String apiKey;
    private final String senderAddress;
    private final Map<EmailType, EmailTypeSettings> emails;
    private final boolean fakeEmails;

    public enum EmailType {
        VERIFY_EMAIL_ADDRESS,
        GENERATION_COMPLETED,
        GENERATION_FAILED
    }

    public record EmailTypeSettings(Long templateId) {}
}
