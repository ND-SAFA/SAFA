package edu.nd.crc.safa.test.features.users;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.organizations.entities.app.OrganizationAppEntity;
import edu.nd.crc.safa.features.organizations.entities.db.PaymentTier;
import edu.nd.crc.safa.features.organizations.services.OrganizationService;
import edu.nd.crc.safa.features.users.controllers.SafaUserController;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
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
    private OrganizationService organizationService;

    @Test
    public void testRegularUserCannotPerformSuperuserAction() throws JsonProcessingException {
        performSuperuserAction(false);
    }

    @Test
    public void testUnactivatedSuperuserCannotPerformSuperuserAction() throws JsonProcessingException {
        rootBuilder.getCommonRequestService().user().makeUserSuperuser(getCurrentUser());
        performSuperuserAction(false);
    }

    @Test
    public void testDeactivatedSuperuserCannotPerformSuperuserAction() throws Exception {
        rootBuilder.getCommonRequestService().user()
            .makeUserSuperuser(getCurrentUser())
            .activateSuperuser()
            .deactivateSuperuser();
        performSuperuserAction(false);
    }

    @Test
    public void testActivatedSuperuserCanPerformSuperuserAction() throws Exception {
        rootBuilder.getCommonRequestService().user()
            .makeUserSuperuser(getCurrentUser())
            .activateSuperuser();
        performSuperuserAction(true);
    }

    @Test
    public void testMakeOtherUserSuperuser() throws Exception {
        String newUserEmail = "new@user.com";
        String newUserPassword = "newuserpassword";

        rootBuilder.getAuthorizationTestService()
            .createUser(newUserEmail, newUserPassword);

        rootBuilder.getCommonRequestService().user()
            .makeUserSuperuser(getCurrentUser())
            .activateSuperuser();
        SafaRequest.withRoute(AppRoutes.Accounts.SuperUser.ROOT)
            .putWithJsonObject(new SafaUserController.CreateSuperUserDTO(newUserEmail));
        rootBuilder.getCommonRequestService().user().deactivateSuperuser();

        rootBuilder.getAuthorizationTestService().loginUser(newUserEmail, newUserPassword, this);
        rootBuilder.getCommonRequestService().user().activateSuperuser();
        performSuperuserAction(true);
    }

    @Test
    public void testAddingAdminUpdatesPaymentTier() {
        String newUserEmail = "new@user.com";
        String newUserPassword = "newuserpassword";

        rootBuilder.getAuthorizationTestService()
            .createUser(newUserEmail, newUserPassword);

        rootBuilder.getCommonRequestService().user()
            .makeUserSuperuser(getCurrentUser())
            .activateSuperuser();
        SafaRequest.withRoute(AppRoutes.Accounts.SuperUser.ROOT)
            .putWithJsonObject(new SafaUserController.CreateSuperUserDTO(newUserEmail));
        rootBuilder.getCommonRequestService().user().deactivateSuperuser();

        SafaUser otherUser = getServiceProvider().getSafaUserService().getUserByEmail(newUserEmail);

        assertThat(organizationService.getPersonalOrganization(otherUser).getPaymentTier())
            .isEqualTo(PaymentTier.UNLIMITED);
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
