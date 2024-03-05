package edu.nd.crc.safa.test.features.billing;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.time.Period;
import java.util.List;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.billing.entities.app.TransactionAppEntity;
import edu.nd.crc.safa.features.billing.entities.db.Transaction;
import edu.nd.crc.safa.features.billing.repositories.TransactionRepository;
import edu.nd.crc.safa.features.billing.services.TransactionService;
import edu.nd.crc.safa.features.memberships.services.OrganizationMembershipService;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.services.OrganizationService;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import com.fasterxml.jackson.core.type.TypeReference;
import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

public class TestGetTransactionList extends ApplicationBaseTest {

    @Autowired
    private TransactionService transactionService;

    @Autowired
    private TransactionRepository transactionRepository;

    @Autowired
    private OrganizationService organizationService;

    @Autowired
    private OrganizationMembershipService orgMembershipService;

    private Organization otherOrg;

    @BeforeEach
    public void setup() {
        Organization personalOrg = organizationService.getPersonalOrganization(getCurrentUser());
        otherOrg = dbEntityBuilder.newOrganization("test org", "desc");

        doTransaction(personalOrg, 10);
        doTransaction(otherOrg, 15);

        doOldTransaction(personalOrg, 1);
        doOldTransaction(otherOrg, 2);
    }


    @Test
    public void testGetPersonalTransactions() throws Exception {
        List<TransactionAppEntity> transactions =
            SafaRequest.withRoute(AppRoutes.Billing.Transaction.ROOT)
                .getAsType(new TypeReference<>(){});

        assertThat(transactions.size()).isEqualTo(2);
        assertThat(transactions.stream().anyMatch(t -> t.getAmount() == 10)).isTrue();
        assertThat(transactions.stream().anyMatch(t -> t.getAmount() == 1)).isTrue();
    }

    @Test
    public void testGetOrgTransactions() throws Exception {
        List<TransactionAppEntity> transactions =
            SafaRequest.withRoute(AppRoutes.Billing.Transaction.BY_ORG)
                .withOrgId(otherOrg.getId())
                .getAsType(new TypeReference<>(){});

        assertThat(transactions.size()).isEqualTo(2);
        assertThat(transactions.stream().anyMatch(t -> t.getAmount() == 15)).isTrue();
        assertThat(transactions.stream().anyMatch(t -> t.getAmount() == 2)).isTrue();
    }

    @Test
    public void testGetOrgTransactionsWithoutPermission() throws Exception {
        leaveOrg();
        JSONObject response =
            SafaRequest.withRoute(AppRoutes.Billing.Transaction.BY_ORG)
                .withOrgId(otherOrg.getId())
                .getWithJsonObject(status().is4xxClientError());

        assertThat(response.has("permissions")).isTrue();
        assertThat(jsonArrayContains(response.getJSONArray("permissions"), "org.view_billing")).isTrue();
    }

    @Test
    public void testGetPersonalMonthlyTransactions() throws Exception {
        List<TransactionAppEntity> transactions =
            SafaRequest.withRoute(AppRoutes.Billing.Transaction.MONTHLY)
                .getAsType(new TypeReference<>(){});

        assertThat(transactions.size()).isEqualTo(1);
        assertThat(transactions.stream().anyMatch(t -> t.getAmount() == 10)).isTrue();
    }

    @Test
    public void testGetOrgMonthlyTransactions() throws Exception {
        List<TransactionAppEntity> transactions =
            SafaRequest.withRoute(AppRoutes.Billing.Transaction.BY_ORG_MONTHLY)
                .withOrgId(otherOrg.getId())
                .getAsType(new TypeReference<>(){});

        assertThat(transactions.size()).isEqualTo(1);
        assertThat(transactions.stream().anyMatch(t -> t.getAmount() == 15)).isTrue();
    }

    @Test
    public void testGetOrgMonthlyTransactionsWithoutPermission() throws Exception {
        leaveOrg();
        JSONObject response =
            SafaRequest.withRoute(AppRoutes.Billing.Transaction.BY_ORG_MONTHLY)
                .withOrgId(otherOrg.getId())
                .getWithJsonObject(status().is4xxClientError());

        assertThat(response.has("permissions")).isTrue();
        assertThat(jsonArrayContains(response.getJSONArray("permissions"), "org.view_billing")).isTrue();
    }

    private boolean jsonArrayContains(JSONArray array, String value) {
        for (int i = 0; i < array.length(); ++i) {
            if (array.getString(i).equals(value)) {
                return true;
            }
        }
        return false;
    }

    private void leaveOrg() {
        orgMembershipService.getOrganizationMembershipsForUser(getCurrentUser())
            .stream()
            .filter(m -> m.getOrganization().getId().equals(otherOrg.getId()))
            .forEach(m -> orgMembershipService.removeUserRole(getCurrentUser(), m.getOrganization(), m.getRole()));
    }

    private Transaction doTransaction(Organization org, int amount) {
        Transaction transaction = transactionService.credit(org, amount, "test transaction");
        return transactionService.markTransactionSuccessful(transaction);
    }

    private void doOldTransaction(Organization org, int amount) {
        Transaction transaction = doTransaction(org, amount);
        transaction.setTimestamp(transaction.getTimestamp().minus(Period.ofMonths(1)));
        transactionRepository.save(transaction);
    }
}
