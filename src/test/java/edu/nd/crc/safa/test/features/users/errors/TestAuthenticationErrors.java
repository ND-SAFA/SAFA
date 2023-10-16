package edu.nd.crc.safa.test.features.users.errors;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.junit.jupiter.api.Test;

class TestAuthenticationErrors extends ApplicationBaseTest {
    @Test
    void testMissingCredentials() throws Exception {
        SafaRequest.clearAuthorizationToken();
        SafaRequest
            .withRoute(AppRoutes.Projects.GET_PROJECTS)
            .getWithJsonObject(status().isUnauthorized());
    }

    @Test
    void testForbiddenIsUserNotAuthorized() throws Exception {
        String testEmail = "test@123.com";
        String testPassword = "testpassword";
        authorizationService.loginUser(testEmail, testPassword, status().is4xxClientError(), false, this);
    }
}
