package edu.nd.crc.safa.test.features.billing;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.assertj.core.api.AssertionsForClassTypes.assertThatThrownBy;

import edu.nd.crc.safa.features.billing.entities.InsufficientFundsException;
import edu.nd.crc.safa.features.billing.entities.db.BillingInfo;
import edu.nd.crc.safa.features.billing.repositories.BillingInfoRepository;
import edu.nd.crc.safa.features.billing.services.BillingService;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.services.OrganizationService;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

public class TestBillingService extends ApplicationBaseTest {

    @Autowired
    private BillingService billingService;

    @Autowired
    private BillingInfoRepository billingInfoRepository;

    @Autowired
    private OrganizationService organizationService;

    @Test
    public void testBillingInfoRetrieval() {
        Organization myOrg = organizationService.getPersonalOrganization(getCurrentUser());

        // Test that something is retrieved without having to do any insertions
        BillingInfo billingInfo = billingService.getBillingInfoForOrg(myOrg);
        assertThat(billingInfo).isNotNull();
        assertThat(billingInfo.getOrganization()).isEqualTo(myOrg);

        // Make a modification and test that it is reflected in later retrievals
        int newBalance = 42;
        billingInfo.setBalance(newBalance);
        billingInfoRepository.save(billingInfo);

        BillingInfo updatedBillingInfo = billingService.getBillingInfoForOrg(myOrg);
        assertThat(updatedBillingInfo).isNotNull();
        assertThat(updatedBillingInfo.getBalance()).isEqualTo(newBalance);
    }

    @Test
    public void testSimpleTransactionUpdatesBalance() {
        Organization myOrg = organizationService.getPersonalOrganization(getCurrentUser());

        billingService.credit(myOrg, 100);
        assertBalance(myOrg, 100);

        billingService.charge(myOrg, 25);
        assertBalance(myOrg, 75);
    }

    @Test
    public void testBalanceCannotGoNegative() {
        Organization myOrg = organizationService.getPersonalOrganization(getCurrentUser());

        int balance = 10;
        int charge = 100;

        billingService.credit(myOrg, balance);

        InsufficientFundsException expected = new InsufficientFundsException(balance, charge);
        assertThatThrownBy(() -> billingService.charge(myOrg, charge))
            .isInstanceOf(InsufficientFundsException.class)
            .isEqualTo(expected);
    }

    @Test
    public void testTransactionAmountMustBePositive() {
        Organization myOrg = organizationService.getPersonalOrganization(getCurrentUser());

        assertThatThrownBy(() -> billingService.charge(myOrg, -1))
            .isInstanceOf(IllegalArgumentException.class)
            .hasMessageContaining("Amount cannot be negative");

        assertThatThrownBy(() -> billingService.credit(myOrg, -1))
            .isInstanceOf(IllegalArgumentException.class)
            .hasMessageContaining("Amount cannot be negative");

        assertThatThrownBy(() -> billingService.charge(myOrg, 0))
            .isInstanceOf(IllegalArgumentException.class)
            .hasMessageContaining("Amount cannot be zero");

        assertThatThrownBy(() -> billingService.credit(myOrg, 0))
            .isInstanceOf(IllegalArgumentException.class)
            .hasMessageContaining("Amount cannot be zero");
    }

    private void assertBalance(Organization organization, int balance) {
        BillingInfo billingInfo = billingService.getBillingInfoForOrg(organization);
        assertThat(billingInfo.getBalance()).isEqualTo(balance);
    }
}
