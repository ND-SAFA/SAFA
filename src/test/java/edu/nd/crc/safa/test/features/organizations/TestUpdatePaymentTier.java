package edu.nd.crc.safa.test.features.organizations;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.billing.controllers.BillingController;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.PaymentTier;
import edu.nd.crc.safa.features.organizations.services.OrganizationService;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.web.servlet.ResultMatcher;

public class TestUpdatePaymentTier extends ApplicationBaseTest {

    @Autowired
    private OrganizationService organizationService;

    @BeforeEach
    public void makeUserSuperuser() {
        rootBuilder.getCommonRequestService().user().makeUserSuperuser(getCurrentUser());
    }

    @Test
    public void testUpdatePaymentTier() {
        Organization selfOrg = getSelfOrg();
        setSuperuser(true);

        for (PaymentTier tier : PaymentTier.values()) {
            updateOrg(selfOrg, tier, true);
            selfOrg = getSelfOrg();
            assertThat(selfOrg.getPaymentTier()).isEqualTo(tier);
        }
    }

    @Test
    public void testUpdateFailsWhenNoActiveSuperuser() {
        Organization selfOrg = getSelfOrg();
        PaymentTier originalTier = selfOrg.getPaymentTier();
        setSuperuser(false);

        for (PaymentTier tier : PaymentTier.values()) {
            updateOrg(selfOrg, tier, false);
            selfOrg = getSelfOrg();
            assertThat(selfOrg.getPaymentTier()).isEqualTo(originalTier);
        }
    }

    private void updateOrg(Organization organization, PaymentTier paymentTier, boolean succeed) {
        ResultMatcher resultMatcher;
        if (succeed) {
            resultMatcher = status().is2xxSuccessful();
        } else {
            resultMatcher = status().is4xxClientError();
        }

        BillingController.ChangePaymentTierDTO requestBody =
                new BillingController.ChangePaymentTierDTO(organization.getId(), paymentTier);
        SafaRequest.withRoute(AppRoutes.Billing.CHANGE_TIER).putWithJsonObject(requestBody, resultMatcher);
    }

    private Organization getSelfOrg() {
        return organizationService.getPersonalOrganization(getCurrentUser());
    }

    private void setSuperuser(boolean on) {
        if (on) {
            rootBuilder.getCommonRequestService().user().activateSuperuser();
        } else {
            rootBuilder.getCommonRequestService().user().deactivateSuperuser();
        }
    }
}
