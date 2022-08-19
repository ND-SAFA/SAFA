package features.users.crud;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.Optional;

import requests.SafaRequest;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.repositories.SafaUserRepository;

import features.users.base.AbstractUserTest;
import org.json.JSONArray;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

/**
 * Tests that user is able to:
 * 1. Create an account.
 * 2. Log into an existing account
 * 3. User is not allowed without credentials.
 */
class TestCreateAndLogin extends AbstractUserTest {


    @Autowired
    SafaUserRepository safaUserRepository;


    @Test
    void testCreateAccount() throws Exception {
        authorizationTestService.createUser(testEmail, testPassword);
        Optional<SafaUser> userQuery = safaUserRepository.findByEmail(testEmail);
        assertThat(userQuery).isPresent();

        SafaUser user = userQuery.get();
        assertThat(user.getEmail()).isEqualTo(testEmail);
    }


    @Test
    void testLogin() throws Exception {
        authorizationTestService.createUser(testEmail, testPassword);
        authorizationTestService.loginUser(testEmail, testPassword, status().isOk());

        // VP - Verify that user is able to be authenticated and no projects are assigned to it.
        JSONArray response = new SafaRequest(AppRoutes.Projects.GET_PROJECTS).getWithJsonArray();
        assertThat(response.length()).isZero();
    }
}
