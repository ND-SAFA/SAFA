package edu.nd.crc.safa.test.features.users;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.users.controllers.SafaUserController;
import edu.nd.crc.safa.features.users.entities.app.CreateAccountRequest;
import edu.nd.crc.safa.features.users.entities.app.UserAppEntity;
import edu.nd.crc.safa.features.users.entities.db.EmailVerificationToken;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.repositories.EmailVerificationTokenRepository;
import edu.nd.crc.safa.features.users.services.SafaUserService;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import com.fasterxml.jackson.core.type.TypeReference;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

public class TestVerifyAccount extends ApplicationBaseTest {

    @Autowired
    private EmailVerificationTokenRepository tokenRepository;

    @Autowired
    private SafaUserService safaUserService;

    @BeforeEach
    public void mockEmailSend() throws Exception {
        tokenRepository.deleteAll();
    }

    @Test
    public void testVerifyAccount() throws Exception {
        CreateAccountRequest createAccountRequest = new CreateAccountRequest();
        createAccountRequest.setEmail("test@example.com");
        createAccountRequest.setPassword("test123");

        UserAppEntity userIdentifier = new SafaRequest(AppRoutes.Accounts.CREATE_ACCOUNT)
            .postAndParseResponse(createAccountRequest, new TypeReference<>() {});

        EmailVerificationToken tokenEntry = tokenRepository.findByUserUserId(userIdentifier.getUserId());
        String token = tokenEntry.getToken();

        new SafaRequest(AppRoutes.Accounts.VERIFY_ACCOUNT)
            .postWithJsonObject(new SafaUserController.AccountVerificationDTO(token));

        SafaUser user = safaUserService.getUserById(userIdentifier.getUserId());
        assertThat(user.isVerified()).isTrue();
    }

    @Test
    public void testVerificationFailsWithBadToken() throws Exception {
        CreateAccountRequest createAccountRequest = new CreateAccountRequest();
        createAccountRequest.setEmail("test@example.com");
        createAccountRequest.setPassword("test123");

        new SafaRequest(AppRoutes.Accounts.CREATE_ACCOUNT)
            .postAndParseResponse(createAccountRequest, new TypeReference<>() {});

        new SafaRequest(AppRoutes.Accounts.VERIFY_ACCOUNT)
            .postWithJsonObject(
                new SafaUserController.AccountVerificationDTO("NOT THE RIGHT TOKEN"),
                status().is4xxClientError()
            );
    }
}
