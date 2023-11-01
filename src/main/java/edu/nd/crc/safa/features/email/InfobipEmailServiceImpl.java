package edu.nd.crc.safa.features.email;

import java.io.IOException;
import java.util.List;
import java.util.concurrent.Callable;
import javax.annotation.PostConstruct;

import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.utilities.FileUtilities;

import com.infobip.ApiClient;
import com.infobip.ApiKey;
import com.infobip.BaseUrl;
import com.infobip.api.EmailApi;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Service;

/**
 * {@link EmailService} implementation using Infobip's email API.
 */
@Service
@ConditionalOnProperty(
    value = "email.provider",
    havingValue = "infobip",
    matchIfMissing = true
)
public class InfobipEmailServiceImpl implements EmailService {

    private static final Logger log = LoggerFactory.getLogger(InfobipEmailServiceImpl.class.getName());

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

    // TODO this is unused until we can implement Infobip
    //      templates, which is blocked by this issue:
    //      https://github.com/infobip/infobip-api-java-client/issues/37
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
        wrapSendEmail(() -> {
            String url = String.format(fendBase + verifyEmailUrl, token);
            String emailTemplate = getVerificationEmailTemplate();
            String emailText = String.format(emailTemplate, url);

            return emailApi
                .sendEmail(List.of(recipient))
                .from(senderEmailAddress)
                .subject("Verify your email")
                .html(emailText)
                .execute();
        });
    }

    /**
     * Wrap an email send call in a try catch for consistent error handling.
     *
     * @param emailSendFunction The function to send the email
     * @return Whatever the email send function returns
     * @param <T> The type of the parameter returned by the email send function
     */
    private <T> T wrapSendEmail(Callable<T> emailSendFunction) {
        try {
            return emailSendFunction.call();
        } catch (Exception e) {
            throw new SafaError("Failed to send email", e);
        }
    }

    /**
     * Get a template email for email verification. This wraps the call to
     * load the template from the classpath so that if there are any errors,
     * a default value is used and the email will still get sent.
     *
     * @return The text of the email template
     */
    private String getVerificationEmailTemplate() {
        try {
            return FileUtilities.readClasspathFile("verification-email-template.html");
        } catch (IOException e) {
            log.warn("Failed to get verification email template", e);
            return "Please use this link to verify your email: %s";
        }
    }
}
