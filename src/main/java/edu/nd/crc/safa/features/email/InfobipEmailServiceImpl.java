package edu.nd.crc.safa.features.email;


import javax.annotation.PostConstruct;

import edu.nd.crc.safa.features.projects.entities.app.SafaError;

import com.infobip.ApiClient;
import com.infobip.ApiException;
import com.infobip.api.SendEmailApi;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
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

    private static final Logger log = LoggerFactory.getLogger(InfobipEmailServiceImpl.class);

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

    private SendEmailApi sendEmailApi;

    @PostConstruct
    public void init() {
        ApiClient client = new ApiClient();

        client.setApiKeyPrefix("App");
        client.setApiKey(infobipKey);
        client.setBasePath(infobipEndpoint);
        this.sendEmailApi = new SendEmailApi(client);
    }

    @Override
    public void sendPasswordReset(String recipient, String token) {
        try {
            sendEmailApi.sendEmail(senderEmailAddress, recipient, "Requested password reset token")
                .text(String.format(fendBase + resetPasswordUrl, token))
                .execute();
        } catch (ApiException e) {
            throw new SafaError("Failed to send email", e);
        }
    }

}
