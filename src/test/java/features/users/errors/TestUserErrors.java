package features.users.errors;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.builders.requests.SafaRequest;
import edu.nd.crc.safa.config.AppRoutes;

import features.users.base.AbstractUserTest;
import org.junit.jupiter.api.Test;

class TestUserErrors extends AbstractUserTest {
    @Test
    void testInvalidRequestMissingCredentials() throws Exception {
        SafaRequest.clearAuthorizationToken();
        SafaRequest
            .withRoute(AppRoutes.Projects.GET_PROJECTS)
            .getWithJsonObject(status().isForbidden());
    }

    @Test
    void testForbiddenIsUserNotAuthorized() throws Exception {
        authorizationTestService.loginUser(testEmail, testPassword, status().is4xxClientError(), false);
    }
}
