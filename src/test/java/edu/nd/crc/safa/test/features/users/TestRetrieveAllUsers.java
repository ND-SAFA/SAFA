package edu.nd.crc.safa.test.features.users;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.HashSet;
import java.util.List;
import java.util.Set;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.users.entities.app.UserAppEntity;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import com.fasterxml.jackson.core.type.TypeReference;
import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;

public class TestRetrieveAllUsers extends ApplicationBaseTest {

    @Test
    public void testMissingPermission() throws Exception {
        JSONObject response = SafaRequest.withRoute(AppRoutes.Accounts.ROOT)
                .getWithoutBody(status().is4xxClientError());
        assertThat(response.has("permissions")).isTrue();
        JSONArray missingPermissions = response.getJSONArray("permissions");
        assertThat(missingPermissions.length()).isEqualTo(1);
        assertThat(missingPermissions.getString(0)).isEqualTo("safa.superuser");
    }

    @Test
    public void testGetAllUsers() throws Exception {
        UserAppEntity secondUser = rootBuilder
                .authorize(a -> a.createUser("seconduser@email.test", "seconduserpassword"))
                .get().get();

        rootBuilder.getCommonRequestService().user().makeUserSuperuser(getCurrentUser());

        List<UserAppEntity> users = SafaRequest.withRoute(AppRoutes.Accounts.ROOT)
                .getAsType(new TypeReference<>() {});

        Set<String> expectedUsers = new HashSet<>(Set.of(currentUserName, secondUser.getEmail()));

        for (UserAppEntity user : users) {
            assertThat(expectedUsers.contains(user.getEmail())).isTrue();
            expectedUsers.remove(user.getEmail());
        }

        assertThat(expectedUsers.size()).isEqualTo(0);
    }
}
