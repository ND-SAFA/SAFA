package edu.nd.crc.safa.test.features.users.crud;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.Optional;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.users.entities.app.UserPasswordDTO;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.SafaRequest;
import edu.nd.crc.safa.utilities.JsonFileUtilities;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;

/**
 * Tests the ability of a user to delete their account
 */
class TestDeleteAccount extends ApplicationBaseTest {
    /**
     * Creates new account, verifies it exists, deletes it, and verifies
     * that it is deleted.
     *
     * @throws Exception If HTTP request fails.
     */
    @Test
    void testDeleteAccount() throws Exception {
        // VP - Verify account exists
        Optional<SafaUser> safaUserOptional = this.safaUserRepository.findByEmail(currentUserName);
        assertThat(safaUserOptional).isPresent();

        // Step 2 - Delete account
        UserPasswordDTO userPasswordDTO = new UserPasswordDTO(defaultUserPassword);
        JSONObject userJson = JsonFileUtilities.toJson(userPasswordDTO);
        SafaRequest
            .withRoute(AppRoutes.Accounts.DELETE_ACCOUNT)
            .postWithJsonObject(userJson);

        // VP - Verify account does not exist
        safaUserOptional = this.safaUserRepository.findByEmail(currentUserName);
        assertThat(safaUserOptional).isEmpty();
    }
}
