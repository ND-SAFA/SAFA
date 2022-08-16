package features.users.logic;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.builders.requests.SafaRequest;

import features.users.base.AbstractUserTest;
import org.junit.jupiter.api.Test;

/**
 * Test that creating a user and performing login using
 * internal methods sets the authorization token.
 */
class TestUserToken extends AbstractUserTest {
    @Test
    void createAndLoginUser() throws Exception {
        authorizationTestService.createUser(testEmail, testPassword);
        authorizationTestService.loginUser(testEmail, testPassword, status().isOk());
        assertThat(SafaRequest.getAuthorizationToken()).isNotNull();
    }
}
