package edu.nd.crc.safa.test.features.billing;

import static org.assertj.core.api.Assertions.within;
import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.assertj.core.api.AssertionsForClassTypes.assertThatThrownBy;

import java.time.LocalDateTime;
import java.time.temporal.ChronoUnit;

import edu.nd.crc.safa.features.billing.entities.InsufficientFundsException;
import edu.nd.crc.safa.features.billing.entities.MonthlyUsage;
import edu.nd.crc.safa.features.billing.entities.db.BillingInfo;
import edu.nd.crc.safa.features.billing.entities.db.Transaction;
import edu.nd.crc.safa.features.billing.repositories.BillingInfoRepository;
import edu.nd.crc.safa.features.billing.repositories.TransactionRepository;
import edu.nd.crc.safa.features.billing.services.BillingService;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.services.OrganizationService;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

public class TestBillingService extends ApplicationBaseTest {

    @Autowired
    private BillingService billingService;

    @Autowired
    private BillingInfoRepository billingInfoRepository;

    @Autowired
    private TransactionRepository transactionRepository;

    @Autowired
    private OrganizationService organizationService;

    private Organization myOrg;

    @BeforeEach
    public void setup() {
        myOrg = organizationService.getPersonalOrganization(getCurrentUser());
    }

    @Test
    public void testBillingInfoRetrieval() {
        BillingInfo billingInfo = billingService.getBillingInfoForOrg(myOrg);
        assertThat(billingInfo).isNotNull();
        assertThat(billingInfo.getOrganization()).isEqualTo(myOrg);

        int newBalance = 42;
        billingInfo.setBalance(newBalance);
        billingInfoRepository.save(billingInfo);

        BillingInfo updatedBillingInfo = billingService.getBillingInfoForOrg(myOrg);
        assertThat(updatedBillingInfo).isNotNull();
        assertThat(updatedBillingInfo.getBalance()).isEqualTo(newBalance);
    }

    @Test
    public void testSimpleTransactionUpdatesBalance() {
        billingService.credit(myOrg, 100, "test credit");
        assertBalance(myOrg, 100);

        billingService.charge(myOrg, 25, "test charge");
        assertBalance(myOrg, 75);
    }

    @Test
    public void testBalanceCannotGoNegative() {
        int balance = 10;
        int charge = 100;

        billingService.credit(myOrg, balance, "test credit");

        InsufficientFundsException expected = new InsufficientFundsException(balance, charge);
        assertThatThrownBy(() -> billingService.charge(myOrg, charge, "test charge"))
            .isInstanceOf(InsufficientFundsException.class)
            .isEqualTo(expected);
    }

    @Test
    public void testTransactionAmountMustBePositive() {
        assertThatThrownBy(() -> billingService.charge(myOrg, -1, "test charge"))
            .isInstanceOf(IllegalArgumentException.class)
            .hasMessageContaining("Amount cannot be negative");

        assertThatThrownBy(() -> billingService.credit(myOrg, -1, "test charge"))
            .isInstanceOf(IllegalArgumentException.class)
            .hasMessageContaining("Amount cannot be negative");

        assertThatThrownBy(() -> billingService.charge(myOrg, 0, "test charge"))
            .isInstanceOf(IllegalArgumentException.class)
            .hasMessageContaining("Amount cannot be zero");

        assertThatThrownBy(() -> billingService.credit(myOrg, 0, "test charge"))
            .isInstanceOf(IllegalArgumentException.class)
            .hasMessageContaining("Amount cannot be zero");
    }

    private void assertBalance(Organization organization, int balance) {
        BillingInfo billingInfo = billingService.getBillingInfoForOrg(organization);
        assertThat(billingInfo.getBalance()).isEqualTo(balance);
    }

    private void assertBalances(Organization organization, int balance, int totalUsed, int totalSuccessful) {
        BillingInfo billingInfo = billingService.getBillingInfoForOrg(organization);
        assertThat(billingInfo.getBalance()).isEqualTo(balance);
        assertThat(billingInfo.getTotalUsed()).isEqualTo(totalUsed);
        assertThat(billingInfo.getTotalSuccessful()).isEqualTo(totalSuccessful);
    }

    @Test
    public void testTransactionReturnValue() {
        Transaction transaction = billingService.credit(myOrg, 100, "test credit");
        assertThat(transaction).isNotNull();
        assertThat(transaction.getStatus()).isSameAs(Transaction.Status.PENDING);
        assertThat(transaction.getDescription()).isEqualTo("test credit");
        assertThat(transaction.getAmount()).isEqualTo(100);
        assertThat(transaction.getTimestamp()).isCloseTo(LocalDateTime.now(), within(1, ChronoUnit.SECONDS));
        assertThat(transaction.getId()).isNotNull();
        assertThat(transaction.getOrganization()).isEqualTo(myOrg);
    }

    @Test
    public void testMarkPendingTransactionSuccessful() {
        Transaction credit = billingService.credit(myOrg, 100, "test credit");
        Transaction updatedCredit = markSuccessful(credit);

        assertBalances(myOrg, 100, 0, 0);
        assertThat(updatedCredit.getStatus()).isSameAs(Transaction.Status.SUCCESSFUL);

        Transaction charge = billingService.charge(myOrg, 100, "test charge");
        Transaction updatedCharge = markSuccessful(charge);

        assertBalances(myOrg, 0, 100, 100);
        assertThat(updatedCharge.getStatus()).isSameAs(Transaction.Status.SUCCESSFUL);
    }

    @Test
    public void testMarkPendingTransactionFailed() {
        Transaction credit = billingService.credit(myOrg, 100, "test credit");
        Transaction updatedCredit = markFailed(credit);

        assertBalances(myOrg, 0, 0, 0);
        assertThat(updatedCredit.getStatus()).isSameAs(Transaction.Status.FAILED);

        markSuccessful(billingService.credit(myOrg, 100, "test credit"));

        Transaction charge = billingService.charge(myOrg, 100, "test charge");
        Transaction updatedCharge = markFailed(charge);

        assertBalances(myOrg, 100, 100, 0);
        assertThat(updatedCharge.getStatus()).isSameAs(Transaction.Status.FAILED);
    }

    @Test
    public void testMarkPendingTransactionRefunded() {
        Transaction credit = billingService.credit(myOrg, 100, "test credit");
        Transaction updatedCredit = markRefunded(credit);

        assertBalances(myOrg, 0, 0, 0);
        assertThat(updatedCredit.getStatus()).isSameAs(Transaction.Status.REFUNDED);

        markSuccessful(billingService.credit(myOrg, 100, "test credit"));

        Transaction charge = billingService.charge(myOrg, 100, "test charge");
        Transaction updatedCharge = markRefunded(charge);

        assertBalances(myOrg, 100, 0, 0);
        assertThat(updatedCharge.getStatus()).isSameAs(Transaction.Status.REFUNDED);
    }

    @Test
    public void testMarkSuccessfulTransactionFailed() {
        Transaction credit = markSuccessful(billingService.credit(myOrg, 100, "test credit"));

        assertThatThrownBy(() -> markFailed(credit))
            .isInstanceOf(IllegalArgumentException.class);
        assertBalances(myOrg, 100, 0, 0);

        Transaction charge = markSuccessful(billingService.charge(myOrg, 100, "test charge"));

        assertThatThrownBy(() -> markFailed(charge))
            .isInstanceOf(IllegalArgumentException.class);
        assertBalances(myOrg, 0, 100, 100);
    }

    @Test
    public void testMarkSuccessfulTransactionRefunded() {
        Transaction credit = markSuccessful(billingService.credit(myOrg, 100, "test credit"));
        Transaction updatedCredit = markRefunded(credit);

        assertBalances(myOrg, 0, 0, 0);
        assertThat(updatedCredit.getStatus()).isSameAs(Transaction.Status.REFUNDED);

        markSuccessful(billingService.credit(myOrg, 100, "test credit"));

        Transaction charge = markSuccessful(billingService.charge(myOrg, 100, "test charge"));
        Transaction updatedCharge = markRefunded(charge);

        assertBalances(myOrg, 100, 0, 0);
        assertThat(updatedCharge.getStatus()).isSameAs(Transaction.Status.REFUNDED);
    }

    @Test
    public void testMarkFailedTransactionRefunded() {
        Transaction credit = markFailed(billingService.credit(myOrg, 100, "test credit"));
        Transaction updatedCredit = markRefunded(credit);

        assertBalances(myOrg, 0, 0, 0);
        assertThat(updatedCredit.getStatus()).isSameAs(Transaction.Status.REFUNDED);

        markSuccessful(billingService.credit(myOrg, 100, "test credit"));

        Transaction charge = markFailed(billingService.charge(myOrg, 100, "test charge"));
        Transaction updatedCharge = markRefunded(charge);

        assertBalances(myOrg, 100, 0, 0);
        assertThat(updatedCharge.getStatus()).isSameAs(Transaction.Status.REFUNDED);
    }

    @Test
    public void testMarkFailedTransactionSuccessful() {
        Transaction credit = markFailed(billingService.credit(myOrg, 100, "test credit"));

        assertThatThrownBy(() -> markSuccessful(credit))
            .isInstanceOf(IllegalArgumentException.class);
        assertBalances(myOrg, 0, 0, 0);

        markSuccessful(billingService.credit(myOrg, 100, "test credit"));

        Transaction charge = markFailed(billingService.charge(myOrg, 100, "test charge"));

        assertThatThrownBy(() -> markSuccessful(charge))
            .isInstanceOf(IllegalArgumentException.class);
        assertBalances(myOrg, 100, 100, 0);
    }

    @Test
    public void testMarkRefundedTransactionSuccessful() {
        Transaction credit = markRefunded(billingService.credit(myOrg, 100, "test credit"));

        assertThatThrownBy(() -> markSuccessful(credit))
            .isInstanceOf(IllegalArgumentException.class);
        assertBalances(myOrg, 0, 0, 0);

        markSuccessful(billingService.credit(myOrg, 100, "test credit"));

        Transaction charge = markRefunded(billingService.charge(myOrg, 100, "test charge"));

        assertThatThrownBy(() -> markSuccessful(charge))
            .isInstanceOf(IllegalArgumentException.class);
        assertBalances(myOrg, 100, 0, 0);
    }

    @Test
    public void testMarkRefundedTransactionFailed() {
        Transaction credit = markRefunded(billingService.credit(myOrg, 100, "test credit"));

        assertThatThrownBy(() -> markFailed(credit))
            .isInstanceOf(IllegalArgumentException.class);
        assertBalances(myOrg, 0, 0, 0);

        markSuccessful(billingService.credit(myOrg, 100, "test credit"));

        Transaction charge = markRefunded(billingService.charge(myOrg, 100, "test charge"));

        assertThatThrownBy(() -> markFailed(charge))
            .isInstanceOf(IllegalArgumentException.class);
        assertBalances(myOrg, 100, 0, 0);
    }

    @Test
    public void testTotalsWithMultipleTransactions() {
        billingService.credit(myOrg, 10_000_000, "test credit");
        markSuccessful(billingService.credit(myOrg, 1_000_000, "test credit"));
        markFailed(billingService.credit(myOrg, 100_000, "test credit"));
        markRefunded(billingService.credit(myOrg, 10_000, "test credit"));

        assertBalances(myOrg, 11_000_000, 0, 0);

        billingService.charge(myOrg, 1_000, "test credit");
        markSuccessful(billingService.charge(myOrg, 100, "test credit"));
        markFailed(billingService.charge(myOrg, 10, "test credit"));
        markRefunded(billingService.charge(myOrg, 1, "test credit"));

        assertBalances(myOrg, 10_998_900, 110, 100);

        billingService.credit(myOrg, 10_000_000, "test credit");
        markSuccessful(billingService.credit(myOrg, 1_000_000, "test credit"));
        markFailed(billingService.credit(myOrg, 100_000, "test credit"));
        markRefunded(billingService.credit(myOrg, 10_000, "test credit"));

        assertBalances(myOrg, 21_998_900, 110, 100);

        billingService.charge(myOrg, 1_000, "test credit");
        markSuccessful(billingService.charge(myOrg, 100, "test credit"));
        markFailed(billingService.charge(myOrg, 10, "test credit"));
        markRefunded(billingService.charge(myOrg, 1, "test credit"));

        assertBalances(myOrg, 21_997_800, 220, 200);
    }

    private Transaction markFailed(Transaction transaction) {
        return billingService.markTransactionFailed(transaction);
    }

    private Transaction markSuccessful(Transaction transaction) {
        return billingService.markTransactionSuccessful(transaction);
    }

    private Transaction markRefunded(Transaction transaction) {
        return billingService.markTransactionRefunded(transaction);
    }

    @Test
    public void testMonthlyUsageStats() {
        LocalDateTime beforeThisMonth = LocalDateTime.now().minusYears(1);

        markSuccessful(billingService.credit(myOrg, 10_000, "test credit"));

        billingService.charge(myOrg, 1_000, "test charge");
        markSuccessful(billingService.charge(myOrg, 100, "test charge"));
        markFailed(billingService.charge(myOrg, 10, "test charge"));
        markRefunded(billingService.charge(myOrg, 1, "test charge"));

        Transaction pending = billingService.charge(myOrg, 1_000, "test charge");
        Transaction successful = markSuccessful(billingService.charge(myOrg, 100, "test charge"));
        Transaction failed = markFailed(billingService.charge(myOrg, 10, "test charge"));
        Transaction refunded = markRefunded(billingService.charge(myOrg, 1, "test charge"));

        pending.setTimestamp(beforeThisMonth);
        successful.setTimestamp(beforeThisMonth);
        failed.setTimestamp(beforeThisMonth);
        refunded.setTimestamp(beforeThisMonth);

        transactionRepository.save(pending);
        transactionRepository.save(successful);
        transactionRepository.save(failed);
        transactionRepository.save(refunded);

        MonthlyUsage monthlyUsage = billingService.getMonthlyUsageForOrg(myOrg);
        assertThat(monthlyUsage).isNotNull();
        assertThat(monthlyUsage.getUsedCredits()).isEqualTo(110);
        assertThat(monthlyUsage.getSuccessfulCredits()).isEqualTo(100);
    }
}
