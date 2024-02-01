package edu.nd.crc.safa.features.email.services;

import java.util.List;
import java.util.Map;
import java.util.concurrent.Callable;
import javax.annotation.PostConstruct;

import edu.nd.crc.safa.features.email.entities.InfobipProperties;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import com.infobip.ApiClient;
import com.infobip.ApiKey;
import com.infobip.BaseUrl;
import com.infobip.api.EmailApi;
import com.infobip.model.EmailSendResponse;
import lombok.RequiredArgsConstructor;
import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
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
@RequiredArgsConstructor(onConstructor = @__({@Autowired}))
public class InfobipEmailServiceImpl implements EmailService {

    private static final Logger log = LoggerFactory.getLogger(InfobipEmailServiceImpl.class.getName());

    private final InfobipProperties infobipProperties;

    @Value("${fend.base}")
    private String fendBase;

    @Value("${fend.reset-email-path}")
    private String resetPasswordUrl;

    @Value("${fend.verify-email-path}")
    private String verifyEmailUrl;

    private EmailApi emailApi;

    @PostConstruct
    public void init() {
        ApiClient client = ApiClient.forApiKey(ApiKey.from(infobipProperties.getApiKey()))
            .withBaseUrl(BaseUrl.from(infobipProperties.getEndpoint()))
            .build();

        this.emailApi = new EmailApi(client);
    }

    @Override
    public void sendPasswordReset(String recipient, String token) {
        EmailSendResponse response = wrapSendEmail(() ->
            emailApi
                .sendEmail(List.of(recipient))
                .from(infobipProperties.getSenderAddress())
                .subject("Requested password reset token")
                .text(String.format(fendBase + resetPasswordUrl, token))
                .execute()
        );

        log.info("Password reset email sent to " + recipient + ": " + response);
    }

    @Override
    public void sendEmailVerification(String recipient, String token) {
        String url = String.format(fendBase + verifyEmailUrl, token);
        sendTemplatedEmail(List.of(recipient), InfobipProperties.EmailType.VERIFY_EMAIL_ADDRESS,
            Map.of(
                "accountlink", url
            )
        );
    }

    @Override
    public void sendGenerationCompleted(String recipient, ProjectVersion projectVersion) {
        sendTemplatedEmail(List.of(recipient), InfobipProperties.EmailType.GENERATION_COMPLETED,
            Map.of(
                "jobName", projectVersion.getProject().getName(),
                "projectLink", makeProjectVersionLink(projectVersion)
            )
        );
    }

    @Override
    public void sendGenerationFailed(String recipient, ProjectVersion projectVersion) {
        sendTemplatedEmail(List.of(recipient), InfobipProperties.EmailType.GENERATION_FAILED,
            Map.of(
                "jobName", projectVersion.getProject().getName()
            )
        );
    }

    private String makeProjectVersionLink(ProjectVersion projectVersion) {
        return fendBase + "/project?version=" + projectVersion.getId();
    }

    private void sendTemplatedEmail(List<String> recipients, InfobipProperties.EmailType emailType,
                                    Map<String, String> replacements) {
        EmailSendResponse response = wrapSendEmail(() -> {

            JSONObject placeholdersObject = new JSONObject(replacements);
            Long templateId = infobipProperties.getEmails().get(emailType).templateId();

            return emailApi
                .sendEmail(recipients)
                .from(infobipProperties.getSenderAddress())
                .templateId(templateId)
                .defaultPlaceholders(placeholdersObject.toString())
                .execute();
        });

        log.info(emailType + " email sent to " + recipients + ": " + response);
    }

    /**
     * Wrap an email send call in a try catch for consistent error handling.
     *
     * @param emailSendFunction The function to send the email
     * @param <T> The type of the parameter returned by the email send function
     * @return Whatever the email send function returns
     */
    private <T> T wrapSendEmail(Callable<T> emailSendFunction) {
        try {
            return emailSendFunction.call();
        } catch (Exception e) {
            throw new SafaError("Failed to send email", e);
        }
    }
}
