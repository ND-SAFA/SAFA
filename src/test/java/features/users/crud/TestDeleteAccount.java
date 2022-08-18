package features.users.crud;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.Optional;

import requests.SafaRequest;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.users.entities.app.UserPassword;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.utilities.JsonFileUtilities;

import features.users.base.AbstractUserTest;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;

/**
 * Tests the ability of a user to delete their account
 */
class TestDeleteAccount extends AbstractUserTest {
    /**
     * Creates new account, verifies it exists, deletes it, and verifies
     * that it is deleted.
     *
     * @throws Exception If HTTP request fails.
     */
    @Test
    void testDeleteAccount() throws Exception {
        // Step 1 - Create account
        authorizationTestService.createUser(this.testEmail, this.testPassword);
        authorizationTestService.loginUser(this.testEmail, this.testPassword);

        // VP - Verify account exists
        Optional<SafaUser> safaUserOptional = this.safaUserRepository.findByEmail(this.testEmail);
        assertThat(safaUserOptional).isPresent();

        // Step 2 - Delete account
        UserPassword userPassword = new UserPassword(this.testPassword);
        JSONObject userJson = JsonFileUtilities.toJson(userPassword);
        SafaRequest
            .withRoute(AppRoutes.Accounts.DELETE_ACCOUNT)
            .postWithJsonObject(userJson);

        // VP - Verify account does not exist
        safaUserOptional = this.safaUserRepository.findByEmail(this.testEmail);
        assertThat(safaUserOptional).isEmpty();
    }
}
