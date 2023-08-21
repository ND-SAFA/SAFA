package edu.nd.crc.safa.test.features.memberships.permissions;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import edu.nd.crc.safa.features.organizations.entities.db.ProjectRole;
import edu.nd.crc.safa.test.common.AbstractSharingTest;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;

/**
 * Tests that test that a permission's error occurs on defined operations.
 */
public abstract class AbstractPermissionViolationTest extends AbstractSharingTest {

    /**
     * @return {@link JSONObject} representing response of violating action.
     * @throws Exception If http error occurs.
     */
    protected abstract JSONObject performViolatingAction() throws Exception;

    /**
     * @return {@link ProjectRole} representing role sharee is supposed to have to achieve action.
     */
    protected abstract ProjectRole getExpectedRole();

    @Test
    protected void attemptProjectEdit() throws Exception {
        // Step - Log in as other user
        authorizationService.loginUser(Sharee.email, Sharee.password, true);

        // Step - Perform violating action
        String message = performViolatingAction().getString("message");

        // VP - Verify that message contains
        assertThat(message)
            .containsIgnoringCase(getExpectedRole().toString())
            .containsIgnoringCase("permission");
    }
}
