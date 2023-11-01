package edu.nd.crc.safa.features.email;

import java.util.List;
import java.util.concurrent.Callable;
import javax.annotation.PostConstruct;

import edu.nd.crc.safa.features.projects.entities.app.SafaError;

import com.infobip.ApiClient;
import com.infobip.ApiKey;
import com.infobip.BaseUrl;
import com.infobip.api.EmailApi;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Service;

/**
 * {@link EmailService} implementation using Infobip's email API. However, it's the default implementation for now
 * to be used if another one is not chosen
 */
@Service
@ConditionalOnProperty(
    value = "email.provider",
    havingValue = "infobip",
    matchIfMissing = true
)
public class InfobipEmailServiceImpl implements EmailService {

    @Value("${email.infobip.endpoint}")
    private String infobipEndpoint;

    @Value("${email.infobip.key}")
    private String infobipKey;

    @Value("${email.infobip.sender-address}")
    private String senderEmailAddress;

    @Value("${fend.base}")
    private String fendBase;

    @Value("${fend.reset-email-path}")
    private String resetPasswordUrl;

    @Value("${fend.verify-email-path}")
    private String verifyEmailUrl;

    @Value("${email.infobip.verify-email-template-id}")
    private Long verifyEmailTemplateId;

    private EmailApi emailApi;

    @PostConstruct
    public void init() {
        ApiClient client = ApiClient.forApiKey(ApiKey.from(infobipKey))
            .withBaseUrl(BaseUrl.from(infobipEndpoint))
            .build();

        this.emailApi = new EmailApi(client);
    }

    @Override
    public void sendPasswordReset(String recipient, String token) {
        wrapSendEmail(() ->
            emailApi
                .sendEmail(List.of(recipient))
                .from(senderEmailAddress)
                .subject("Requested password reset token")
                .text(String.format(fendBase + resetPasswordUrl, token))
                .execute()
        );
    }

    @Override
    public void sendEmailVerification(String recipient, String token) {
        wrapSendEmail(() ->
            emailApi
                .sendEmail(List.of(recipient))
                .from(senderEmailAddress)
                .subject("Verify your email")
                .text(String.format(fendBase + verifyEmailUrl, token))
                .execute()
        );
    }

    private <T> T wrapSendEmail(Callable<T> emailSendFunction) {
        try {
            return emailSendFunction.call();
        } catch (Exception e) {
            throw new SafaError("Failed to send email", e);
        }
    }
}
