package edu.nd.crc.safa.test.features.memberships.errors;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.features.organizations.entities.db.ProjectRole;
import edu.nd.crc.safa.test.common.AbstractSharingTest;
import edu.nd.crc.safa.test.services.requests.CommonProjectRequests;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;

/**
 * Tests that useful error messages are provided for common scenarios including:
 * 1. User is not found
 * 2. User is already on the project
 */
class TestSharingWithMissingAccount extends AbstractSharingTest {
    String nonUserEmail = "non-existing@email.com";

    /**
     * Tests that error message notifies user that email is not registered
     * with an account when sharing to non-linked emails.
     *
     * @throws Exception Throws exception if http fails when sending get request.
     */
    @Test
    void userNotFoundError() throws Exception {
        // Step - Share with non-existent user
        JSONObject response = CommonProjectRequests.addUserToProject(
            project,
            nonUserEmail,
            ProjectRole.VIEWER,
            getCurrentUser(),
            status().is4xxClientError());

        // VP - Verify that error informs that email not associated with account
        String error = response.getString("message");
        assertThat(error).matches(".*user.*exists.*email.*[\\s\\S]");
    }
}
