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
import edu.nd.crc.safa.features.billing.services.CreditBalanceService;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.services.OrganizationService;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

public class TestBalanceTransactionService extends ApplicationBaseTest {

    @Autowired
    private CreditBalanceService creditBalanceService;

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
        BillingInfo billingInfo = creditBalanceService.getBillingInfoForOrg(myOrg);
        assertThat(billingInfo).isNotNull();
        assertThat(billingInfo.getOrganization()).isEqualTo(myOrg);

        int newBalance = 42;
        billingInfo.setBalance(newBalance);
        billingInfoRepository.save(billingInfo);

        BillingInfo updatedBillingInfo = creditBalanceService.getBillingInfoForOrg(myOrg);
        assertThat(updatedBillingInfo).isNotNull();
        assertThat(updatedBillingInfo.getBalance()).isEqualTo(newBalance);
    }

    @Test
    public void testSimpleTransactionUpdatesBalance() {
        // Credits do not count until marked successful, whereas charges are deducted immediately

        Transaction transaction = creditBalanceService.credit(myOrg, 100, "test credit");
        assertBalance(myOrg, 0);
        markSuccessful(transaction);
        assertBalance(myOrg, 100);

        creditBalanceService.charge(myOrg, 25, "test charge");
        assertBalance(myOrg, 75);
    }

    @Test
    public void testBalanceCannotGoNegative() {
        int balance = 10;
        int charge = 100;

        markSuccessful(creditBalanceService.credit(myOrg, balance, "test credit"));

        InsufficientFundsException expected = new InsufficientFundsException(balance, charge);
        assertThatThrownBy(() -> creditBalanceService.charge(myOrg, charge, "test charge"))
            .isInstanceOf(InsufficientFundsException.class)
            .isEqualTo(expected);
    }

    @Test
    public void testTransactionAmountMustBePositive() {
        assertThatThrownBy(() -> creditBalanceService.charge(myOrg, -1, "test charge"))
            .isInstanceOf(IllegalArgumentException.class)
            .hasMessageContaining("Amount cannot be negative");

        assertThatThrownBy(() -> creditBalanceService.credit(myOrg, -1, "test charge"))
            .isInstanceOf(IllegalArgumentException.class)
            .hasMessageContaining("Amount cannot be negative");

        assertThatThrownBy(() -> creditBalanceService.charge(myOrg, 0, "test charge"))
            .isInstanceOf(IllegalArgumentException.class)
            .hasMessageContaining("Amount cannot be zero");

        assertThatThrownBy(() -> creditBalanceService.credit(myOrg, 0, "test charge"))
            .isInstanceOf(IllegalArgumentException.class)
            .hasMessageContaining("Amount cannot be zero");
    }

    private void assertBalance(Organization organization, int balance) {
        BillingInfo billingInfo = creditBalanceService.getBillingInfoForOrg(organization);
        assertThat(billingInfo.getBalance()).isEqualTo(balance);
    }

    private void assertBalances(Organization organization, int balance, int totalUsed, int totalSuccessful) {
        BillingInfo billingInfo = creditBalanceService.getBillingInfoForOrg(organization);
        assertThat(billingInfo.getBalance()).isEqualTo(balance);
        assertThat(billingInfo.getTotalUsed()).isEqualTo(totalUsed);
        assertThat(billingInfo.getTotalSuccessful()).isEqualTo(totalSuccessful);
    }

    @Test
    public void testTransactionReturnValue() {
        Transaction transaction = creditBalanceService.credit(myOrg, 100, "test credit");
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
        Transaction credit = creditBalanceService.credit(myOrg, 100, "test credit");
        Transaction updatedCredit = markSuccessful(credit);

        assertBalances(myOrg, 100, 0, 0);
        assertThat(updatedCredit.getStatus()).isSameAs(Transaction.Status.SUCCESSFUL);

        Transaction charge = creditBalanceService.charge(myOrg, 100, "test charge");
        Transaction updatedCharge = markSuccessful(charge);

        assertBalances(myOrg, 0, 100, 100);
        assertThat(updatedCharge.getStatus()).isSameAs(Transaction.Status.SUCCESSFUL);
    }

    @Test
    public void testMarkPendingTransactionFailed() {
        Transaction credit = creditBalanceService.credit(myOrg, 100, "test credit");
        Transaction updatedCredit = markFailed(credit);

        assertBalances(myOrg, 0, 0, 0);
        assertThat(updatedCredit.getStatus()).isSameAs(Transaction.Status.FAILED);

        markSuccessful(creditBalanceService.credit(myOrg, 100, "test credit"));

        Transaction charge = creditBalanceService.charge(myOrg, 100, "test charge");
        Transaction updatedCharge = markFailed(charge);

        assertBalances(myOrg, 100, 100, 0);
        assertThat(updatedCharge.getStatus()).isSameAs(Transaction.Status.FAILED);
    }

    @Test
    public void testMarkPendingTransactionCanceled() {
        Transaction credit = creditBalanceService.credit(myOrg, 100, "test credit");
        Transaction updatedCredit = markCanceled(credit);

        assertBalances(myOrg, 0, 0, 0);
        assertThat(updatedCredit.getStatus()).isSameAs(Transaction.Status.CANCELED);

        markSuccessful(creditBalanceService.credit(myOrg, 100, "test credit"));

        Transaction charge = creditBalanceService.charge(myOrg, 100, "test charge");
        Transaction updatedCharge = markCanceled(charge);

        assertBalances(myOrg, 100, 0, 0);
        assertThat(updatedCharge.getStatus()).isSameAs(Transaction.Status.CANCELED);
    }

    @Test
    public void testMarkSuccessfulTransactionFailed() {
        Transaction credit = markSuccessful(creditBalanceService.credit(myOrg, 100, "test credit"));

        assertThatThrownBy(() -> markFailed(credit))
            .isInstanceOf(IllegalArgumentException.class);
        assertBalances(myOrg, 100, 0, 0);

        Transaction charge = markSuccessful(creditBalanceService.charge(myOrg, 100, "test charge"));

        assertThatThrownBy(() -> markFailed(charge))
            .isInstanceOf(IllegalArgumentException.class);
        assertBalances(myOrg, 0, 100, 100);
    }

    @Test
    public void testMarkSuccessfulTransactionCanceled() {
        Transaction credit = markSuccessful(creditBalanceService.credit(myOrg, 100, "test credit"));
        Transaction updatedCredit = markCanceled(credit);

        assertBalances(myOrg, 0, 0, 0);
        assertThat(updatedCredit.getStatus()).isSameAs(Transaction.Status.CANCELED);

        markSuccessful(creditBalanceService.credit(myOrg, 100, "test credit"));

        Transaction charge = markSuccessful(creditBalanceService.charge(myOrg, 100, "test charge"));
        Transaction updatedCharge = markCanceled(charge);

        assertBalances(myOrg, 100, 0, 0);
        assertThat(updatedCharge.getStatus()).isSameAs(Transaction.Status.CANCELED);
    }

    @Test
    public void testMarkFailedTransactionCanceled() {
        Transaction credit = markFailed(creditBalanceService.credit(myOrg, 100, "test credit"));
        Transaction updatedCredit = markCanceled(credit);

        assertBalances(myOrg, 0, 0, 0);
        assertThat(updatedCredit.getStatus()).isSameAs(Transaction.Status.CANCELED);

        markSuccessful(creditBalanceService.credit(myOrg, 100, "test credit"));

        Transaction charge = markFailed(creditBalanceService.charge(myOrg, 100, "test charge"));
        Transaction updatedCharge = markCanceled(charge);

        assertBalances(myOrg, 100, 0, 0);
        assertThat(updatedCharge.getStatus()).isSameAs(Transaction.Status.CANCELED);
    }

    @Test
    public void testMarkFailedTransactionSuccessful() {
        Transaction credit = markFailed(creditBalanceService.credit(myOrg, 100, "test credit"));

        assertThatThrownBy(() -> markSuccessful(credit))
            .isInstanceOf(IllegalArgumentException.class);
        assertBalances(myOrg, 0, 0, 0);

        markSuccessful(creditBalanceService.credit(myOrg, 100, "test credit"));

        Transaction charge = markFailed(creditBalanceService.charge(myOrg, 100, "test charge"));

        assertThatThrownBy(() -> markSuccessful(charge))
            .isInstanceOf(IllegalArgumentException.class);
        assertBalances(myOrg, 100, 100, 0);
    }

    @Test
    public void testMarkCanceledTransactionSuccessful() {
        Transaction credit = markCanceled(creditBalanceService.credit(myOrg, 100, "test credit"));

        assertThatThrownBy(() -> markSuccessful(credit))
            .isInstanceOf(IllegalArgumentException.class);
        assertBalances(myOrg, 0, 0, 0);

        markSuccessful(creditBalanceService.credit(myOrg, 100, "test credit"));

        Transaction charge = markCanceled(creditBalanceService.charge(myOrg, 100, "test charge"));

        assertThatThrownBy(() -> markSuccessful(charge))
            .isInstanceOf(IllegalArgumentException.class);
        assertBalances(myOrg, 100, 0, 0);
    }

    @Test
    public void testMarkCanceledTransactionFailed() {
        Transaction credit = markCanceled(creditBalanceService.credit(myOrg, 100, "test credit"));

        assertThatThrownBy(() -> markFailed(credit))
            .isInstanceOf(IllegalArgumentException.class);
        assertBalances(myOrg, 0, 0, 0);

        markSuccessful(creditBalanceService.credit(myOrg, 100, "test credit"));

        Transaction charge = markCanceled(creditBalanceService.charge(myOrg, 100, "test charge"));

        assertThatThrownBy(() -> markFailed(charge))
            .isInstanceOf(IllegalArgumentException.class);
        assertBalances(myOrg, 100, 0, 0);
    }

    @Test
    public void testTotalsWithMultipleTransactions() {
        creditBalanceService.credit(myOrg, 10_000_000, "test credit");
        markSuccessful(creditBalanceService.credit(myOrg, 1_000_000, "test credit"));
        markFailed(creditBalanceService.credit(myOrg, 100_000, "test credit"));
        markCanceled(creditBalanceService.credit(myOrg, 10_000, "test credit"));

        assertBalances(myOrg, 1_000_000, 0, 0);

        creditBalanceService.charge(myOrg, 1_000, "test credit");
        markSuccessful(creditBalanceService.charge(myOrg, 100, "test credit"));
        markFailed(creditBalanceService.charge(myOrg, 10, "test credit"));
        markCanceled(creditBalanceService.charge(myOrg, 1, "test credit"));

        assertBalances(myOrg, 998_900, 110, 100);

        creditBalanceService.credit(myOrg, 10_000_000, "test credit");
        markSuccessful(creditBalanceService.credit(myOrg, 1_000_000, "test credit"));
        markFailed(creditBalanceService.credit(myOrg, 100_000, "test credit"));
        markCanceled(creditBalanceService.credit(myOrg, 10_000, "test credit"));

        assertBalances(myOrg, 1_998_900, 110, 100);

        creditBalanceService.charge(myOrg, 1_000, "test credit");
        markSuccessful(creditBalanceService.charge(myOrg, 100, "test credit"));
        markFailed(creditBalanceService.charge(myOrg, 10, "test credit"));
        markCanceled(creditBalanceService.charge(myOrg, 1, "test credit"));

        assertBalances(myOrg, 1_997_800, 220, 200);
    }

    private Transaction markFailed(Transaction transaction) {
        return creditBalanceService.markTransactionFailed(transaction);
    }

    private Transaction markSuccessful(Transaction transaction) {
        return creditBalanceService.markTransactionSuccessful(transaction);
    }

    private Transaction markCanceled(Transaction transaction) {
        return creditBalanceService.markTransactionCanceled(transaction);
    }

    @Test
    public void testMonthlyUsageStats() {
        LocalDateTime beforeThisMonth = LocalDateTime.now().minusYears(1);

        markSuccessful(creditBalanceService.credit(myOrg, 10_000, "test credit"));

        creditBalanceService.charge(myOrg, 1_000, "test charge");
        markSuccessful(creditBalanceService.charge(myOrg, 100, "test charge"));
        markFailed(creditBalanceService.charge(myOrg, 10, "test charge"));
        markCanceled(creditBalanceService.charge(myOrg, 1, "test charge"));

        Transaction pending = creditBalanceService.charge(myOrg, 1_000, "test charge");
        Transaction successful = markSuccessful(creditBalanceService.charge(myOrg, 100, "test charge"));
        Transaction failed = markFailed(creditBalanceService.charge(myOrg, 10, "test charge"));
        Transaction canceled = markCanceled(creditBalanceService.charge(myOrg, 1, "test charge"));

        pending.setTimestamp(beforeThisMonth);
        successful.setTimestamp(beforeThisMonth);
        failed.setTimestamp(beforeThisMonth);
        canceled.setTimestamp(beforeThisMonth);

        transactionRepository.save(pending);
        transactionRepository.save(successful);
        transactionRepository.save(failed);
        transactionRepository.save(canceled);

        MonthlyUsage monthlyUsage = creditBalanceService.getMonthlyUsageForOrg(myOrg);
        assertThat(monthlyUsage).isNotNull();
        assertThat(monthlyUsage.getUsedCredits()).isEqualTo(110);
        assertThat(monthlyUsage.getSuccessfulCredits()).isEqualTo(100);
    }
}
