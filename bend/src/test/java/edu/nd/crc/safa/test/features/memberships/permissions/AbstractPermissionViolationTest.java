package edu.nd.crc.safa.test.features.memberships.permissions;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.HashSet;
import java.util.Set;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.permissions.entities.Permission;
import edu.nd.crc.safa.test.common.AbstractSharingTest;

import org.json.JSONArray;
import org.json.JSONObject;
import org.springframework.util.function.ThrowingSupplier;

/**
 * Tests that test that a permission's error occurs on defined operations.
 */
public abstract class AbstractPermissionViolationTest extends AbstractSharingTest {

    protected void test(ThrowingSupplier<JSONObject> violatingAction, Set<Permission> expectedPermissions) {
        // Step - Log in as other user
        authorizationService.loginUser(Sharee.email, Sharee.password, true, this);

        // Step - Perform violating action
        JSONObject error = violatingAction.get();

        // VP - Verify that message contains
        assertThat(error.getString("message"))
            .containsIgnoringCase("missing permission");

        Set<String> violatedPermissions = new HashSet<>();
        JSONArray permsArray = error.getJSONArray("permissions");
        for (int i = 0; i < permsArray.length(); ++i) {
            violatedPermissions.add(permsArray.getString(i));
        }

        Set<String> expectedPermissionNames =
            expectedPermissions.stream().map(Permission::getName).collect(Collectors.toSet());
        assertThat(violatedPermissions).isEqualTo(expectedPermissionNames);
    }
}
