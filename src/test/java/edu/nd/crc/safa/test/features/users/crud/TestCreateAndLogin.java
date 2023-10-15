package edu.nd.crc.safa.test.features.users.crud;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.Optional;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;

/**
 * Tests that user is able to:
 * 1. Create an account.
 * 2. Log into an existing account
 * 3. User is not allowed without credentials.
 */
class TestCreateAndLogin extends ApplicationBaseTest {
    String testEmail = "abc@test.com";
    String testPassword = "password123";

    @Test
    void testCreateAccount() throws Exception {
        authorizationService.createUser(testEmail, testPassword);
        Optional<SafaUser> userQuery = safaUserRepository.findByEmail(testEmail);
        assertThat(userQuery).isPresent();

        SafaUser user = userQuery.get();
        assertThat(user.getEmail()).isEqualTo(testEmail);
    }

    @Test
    void testLogin() throws Exception {
        authorizationService.createUser(testEmail, testPassword);
        authorizationService.loginUser(testEmail, testPassword, status().isOk(), this);

        // VP - Verify that user is able to be authenticated and no projects are assigned to it.
        JSONArray response = new SafaRequest(AppRoutes.Projects.GET_PROJECTS).getWithJsonArray();
        assertThat(response.length()).isZero();
    }

    @Test
    void testSelfEndpoint() throws Exception {
        authorizationService.createUser(testEmail, testPassword);
        authorizationService.loginUser(testEmail, testPassword, this);

        JSONObject response = new SafaRequest(AppRoutes.Accounts.SELF).getWithJsonObject(status().isOk());

        assertThat(response.get("email")).isEqualTo(testEmail);
    }

    @Test
    void testCreateDuplicateAccount() throws Exception {
        authorizationService.createUser(testEmail, testPassword, status().is2xxSuccessful());
        authorizationService.createUser(testEmail, testPassword, status().is4xxClientError());
    }
}
