package edu.nd.crc.safa.features.email;

import com.infobip.ApiClient;
import com.infobip.api.ReceiveSmsApi;
import com.infobip.api.SendEmailApi;
import com.infobip.model.EmailSendResponse;
import edu.nd.crc.safa.config.WebApiConfiguration;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.context.annotation.Bean;
import org.springframework.stereotype.Service;

/**
 * {@link EmailService} implementation using Infobip's email API. Also it's the default implementation
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

    @Override
    public void send(String subject, String messageContent, String recipient) throws Exception {
        log.info("Sending email to " + recipient);

        EmailSendResponse emailResponse = sendEmailApi()
            .sendEmail(senderEmailAddress, recipient, subject)
            .text(messageContent)
            .execute();

        log.info("Email response " + emailResponse.toString());
    }

    @Bean
    public SendEmailApi sendEmailApi() {
        ApiClient client = new ApiClient();

        client.setApiKeyPrefix("App");
        client.setApiKey(infobipKey);
        client.setBasePath(infobipEndpoint);
        return new SendEmailApi(client);
    }
}
