package features.users.errors;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.config.AppRoutes;

import features.base.ApplicationBaseTest;
import org.junit.jupiter.api.Test;
import requests.SafaRequest;

class TestAuthenticationErrors extends ApplicationBaseTest {
    @Test
    void testMissingCredentials() throws Exception {
        SafaRequest.clearAuthorizationToken();
        SafaRequest
            .withRoute(AppRoutes.Projects.GET_PROJECTS)
            .getWithJsonObject(status().isForbidden());
    }

    @Test
    void testForbiddenIsUserNotAuthorized() throws Exception {
        String testEmail = "test@123.com";
        String testPassword = "testpassword";
        authorizationTestService.loginUser(testEmail, testPassword, status().is4xxClientError(), false);
    }
}
