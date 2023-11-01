package edu.nd.crc.safa.test.features.users;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.email.EmailService;
import edu.nd.crc.safa.features.users.entities.app.CreateAccountRequest;
import edu.nd.crc.safa.features.users.entities.app.UserIdentifierDTO;
import edu.nd.crc.safa.features.users.entities.db.EmailVerificationToken;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.repositories.EmailVerificationTokenRepository;
import edu.nd.crc.safa.features.users.services.SafaUserService;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import com.fasterxml.jackson.core.type.TypeReference;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.mock.mockito.MockBean;

public class TestVerifyAccount extends ApplicationBaseTest {

    @MockBean
    private EmailService emailService;

    @Autowired
    private EmailVerificationTokenRepository tokenRepository;

    @Autowired
    private SafaUserService safaUserService;

    @BeforeEach
    public void mockEmailSend() throws Exception {
        Mockito.doNothing().when(emailService).sendEmailVerification(
            Mockito.anyString(),
            Mockito.anyString());

        tokenRepository.deleteAll();
    }

    @Test
    public void testVerifyAccount() throws Exception {
        CreateAccountRequest createAccountRequest = new CreateAccountRequest();
        createAccountRequest.setEmail("test@example.com");
        createAccountRequest.setPassword("test123");

        UserIdentifierDTO userIdentifier = new SafaRequest(AppRoutes.Accounts.CREATE_ACCOUNT)
            .postAndParseResponse(createAccountRequest, new TypeReference<>() {});

        EmailVerificationToken tokenEntry = tokenRepository.findByUserUserId(userIdentifier.getUserId());
        String token = tokenEntry.getToken();

        new SafaRequest(AppRoutes.Accounts.VERIFY_ACCOUNT)
            .withQueryParam("token", token)
            .getWithoutBody(status().is2xxSuccessful());

        SafaUser user = safaUserService.getUserById(userIdentifier.getUserId());
        assertThat(user.isVerified()).isTrue();
    }

    @Test
    public void testVerificationFailsWithBadToken() throws Exception {
        CreateAccountRequest createAccountRequest = new CreateAccountRequest();
        createAccountRequest.setEmail("test@example.com");
        createAccountRequest.setPassword("test123");

        UserIdentifierDTO userIdentifier = new SafaRequest(AppRoutes.Accounts.CREATE_ACCOUNT)
            .postAndParseResponse(createAccountRequest, new TypeReference<>() {});

        new SafaRequest(AppRoutes.Accounts.VERIFY_ACCOUNT)
            .withQueryParam("token", "NOT THE RIGHT TOKEN")
            .getWithoutBody(status().is4xxClientError());
    }
}
