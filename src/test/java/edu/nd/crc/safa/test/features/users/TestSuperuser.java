package edu.nd.crc.safa.test.features.users;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.organizations.entities.app.OrganizationAppEntity;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.services.SafaUserService;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.web.servlet.ResultMatcher;

public class TestSuperuser extends ApplicationBaseTest {

    @Autowired
    private SafaUserService safaUserService;

    @Test
    public void testRegularUserCannotPerformSuperuserAction() throws JsonProcessingException {
        performSuperuserAction(false);
    }

    @Test
    public void testUnactivatedSuperuserCannotPerformSuperuserAction() throws JsonProcessingException {
        safaUserService.addSuperUser(getCurrentUser());
        performSuperuserAction(false);
    }

    @Test
    public void testDeactivatedSuperuserCannotPerformSuperuserAction() throws Exception {
        safaUserService.addSuperUser(getCurrentUser());
        safaUserService.setSuperuserActivation(getCurrentUser(), true);
        deactivateSuperuser();
        performSuperuserAction(false);
    }

    @Test
    public void testActivatedSuperuserCanPerformSuperuserAction() throws Exception {
        safaUserService.addSuperUser(getCurrentUser());
        activateSuperuser();
        performSuperuserAction(true);
    }

    @Test
    public void testMakeOtherUserSuperuser() throws Exception {
        String newUserEmail = "new@user.com";
        String newUserPassword = "newuserpassword";

        SafaUser newUser = rootBuilder.getAuthorizationTestService()
            .createUser(newUserEmail, newUserPassword).and()
            .getAccount(newUserEmail);

        safaUserService.addSuperUser(getCurrentUser());
        activateSuperuser();
        SafaRequest.withRoute(AppRoutes.Accounts.SuperUser.BY_USER)
            .withPathVariable("userId", newUser.getUserId().toString())
            .putWithJsonObject(new JSONObject());
        deactivateSuperuser();

        rootBuilder.getAuthorizationTestService().loginUser(newUserEmail, newUserPassword, this);
        assertThat(getCurrentUser().getEmail()).isEqualTo(newUserEmail);

        activateSuperuser();
        performSuperuserAction(true);
    }

    private void activateSuperuser() throws Exception {
        SafaRequest.withRoute(AppRoutes.Accounts.SuperUser.ACTIVATE)
            .putWithJsonObject(new JSONObject());
    }

    private void deactivateSuperuser() throws Exception {
        SafaRequest.withRoute(AppRoutes.Accounts.SuperUser.DEACTIVATE)
            .putWithJsonObject(new JSONObject());
    }

    private void performSuperuserAction(boolean shouldSucceed) throws JsonProcessingException {
        ResultMatcher resultMatcher;
        if (shouldSucceed) {
            resultMatcher = status().is2xxSuccessful();
        } else {
            resultMatcher = status().is4xxClientError();
        }

        OrganizationAppEntity org = new OrganizationAppEntity("name", "desc");
        JSONObject response = SafaRequest.withRoute(AppRoutes.Organizations.ROOT)
            .postWithJsonObject(org, resultMatcher);

        if (shouldSucceed) {
            OrganizationAppEntity returnedOrg = new ObjectMapper().readValue(response.toString(), new TypeReference<>(){});
            assertThat(returnedOrg.getId()).isNotNull();
        }
    }
}
