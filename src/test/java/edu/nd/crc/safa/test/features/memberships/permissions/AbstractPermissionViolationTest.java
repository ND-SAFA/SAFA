package edu.nd.crc.safa.test.features.memberships.permissions;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.HashSet;
import java.util.Set;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.permissions.entities.Permission;
import edu.nd.crc.safa.test.common.AbstractSharingTest;

import org.json.JSONArray;
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
     * @return {@link Permission} representing permission sharee is supposed to have to achieve action.
     */
    protected abstract Set<Permission> getExpectedPermissions();

    @Test
    protected void attemptViolatingAction() throws Exception {
        // Step - Log in as other user
        authorizationService.loginUser(Sharee.email, Sharee.password, true, this);

        // Step - Perform violating action
        JSONObject error = performViolatingAction();

        // VP - Verify that message contains
        assertThat(error.getString("message"))
            .containsIgnoringCase("missing permission");

        Set<String> violatedPermissions = new HashSet<>();
        JSONArray permsArray = error.getJSONArray("permissions");
        for (int i = 0; i < permsArray.length(); ++i) {
            violatedPermissions.add(permsArray.getString(i));
        }

        Set<String> expectedPermissions =
            getExpectedPermissions().stream().map(Permission::getName).collect(Collectors.toSet());
        assertThat(violatedPermissions).isEqualTo(expectedPermissions);
    }
}
