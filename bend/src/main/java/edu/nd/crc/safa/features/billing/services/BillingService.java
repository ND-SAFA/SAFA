package edu.nd.crc.safa.features.billing.services;

import java.time.LocalDateTime;
import java.time.temporal.ChronoField;
import java.time.temporal.TemporalAdjusters;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.billing.entities.InsufficientFundsException;
import edu.nd.crc.safa.features.billing.entities.MonthlyUsage;
import edu.nd.crc.safa.features.billing.entities.app.TransactionAppEntity;
import edu.nd.crc.safa.features.billing.entities.db.BillingInfo;
import edu.nd.crc.safa.features.billing.entities.db.Transaction;
import edu.nd.crc.safa.features.billing.repositories.BillingInfoRepository;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.PaymentTier;
import edu.nd.crc.safa.features.organizations.services.OrganizationService;

import jakarta.persistence.OptimisticLockException;
import org.springframework.context.annotation.Lazy;
import org.springframework.stereotype.Service;

@Service
public class BillingService {

    private static final int MAX_ACCOUNT_ADJUSTMENT_RETRIES = 5;

    private final BillingInfoRepository billingInfoRepository;
    private final TransactionService transactionService;
    private final IExternalBillingService externalBillingService;
    private final OrganizationService organizationService;

    public BillingService(BillingInfoRepository billingInfoRepository, @Lazy TransactionService transactionService,
                          IExternalBillingService externalBillingService,
                          @Lazy OrganizationService organizationService) {
        this.billingInfoRepository = billingInfoRepository;
        this.transactionService = transactionService;
        this.externalBillingService = externalBillingService;
        this.organizationService = organizationService;
    }

    /**
     * Begin a transaction through an external billing interface
     *
     * @param organization The organization to credit the amount to
     * @param amount The amount to credit
     * @param description A description to attach to the transaction
     * @return A front-end entity containing details about the transaction including the redirect url
     */
    public TransactionAppEntity startTransaction(Organization organization, int amount, String description) {
        Transaction transaction = null;
        
        try {
            transaction = transactionService.credit(organization, amount, description);
            String redirectUrl = externalBillingService.startTransaction(transaction);

            // Save again in case the external service made updates
            transaction = transactionService.saveTransaction(transaction);

            return new TransactionAppEntity(transaction, redirectUrl);
        } catch (Exception e) {
            if (transaction != null) {
                transactionService.markTransactionFailed(transaction);
            }
            throw e;
        }
    }

    /**
     * Finish a transaction with an external interface
     * 
     * @param transactionId The ID of the transaction from {@link #startTransaction(Organization, int, String)}
     */
    public void endTransaction(UUID transactionId) {
        Optional<Transaction> transactionOptional = transactionService.getTransactionOptionalById(transactionId);

        if (transactionOptional.isPresent()) {
            Transaction transaction = transactionOptional.get();
            transaction = transactionService.markTransactionSuccessful(transaction);
            externalBillingService.endTransaction(transaction);

            // Save again in case the external service made updates
            transactionService.saveTransaction(transaction);
        }
    }

    /**
     * Cancel a transaction with an external interface
     *
     * @param transactionId The ID of the transaction from {@link #startTransaction(Organization, int, String)}
     */
    public void cancelTransaction(UUID transactionId) {
        Optional<Transaction> transactionOptional = transactionService.getTransactionOptionalById(transactionId);

        if (transactionOptional.isPresent()) {
            Transaction transaction = transactionOptional.get();
            transaction = transactionService.markTransactionCanceled(transaction);
            externalBillingService.cancelTransaction(transaction);

            // Save again in case the external service made updates
            transactionService.saveTransaction(transaction);
        }
    }

    /**
     * Retrieve billing info for an organization.
     *
     * @param organization The organization to get billing info for
     * @return The billing info for that organization
     */
    public BillingInfo getBillingInfoForOrg(Organization organization) {
        return billingInfoRepository.findByOrganization(organization)
            .orElseGet(() -> {
                BillingInfo billingInfo = new BillingInfo(organization);
                return saveBillingInfo(billingInfo);
            });
    }

    /**
     * Get monthly usage statistics for an organization
     *
     * @param organization The org to get stats for
     * @return The org's stats
     */
    public MonthlyUsage getMonthlyUsageForOrg(Organization organization) {
        LocalDateTime monthStart = LocalDateTime.now()
            .with(TemporalAdjusters.firstDayOfMonth())
            .with(ChronoField.NANO_OF_DAY, 0);
        List<Transaction> thisMonthTransactions = transactionService.getOrgTransactionsAfter(organization, monthStart);

        int usedCredits = 0;
        int successfulCredits = 0;

        for (Transaction transaction : thisMonthTransactions) {
            int usedCreditAmount = transactionService.toUsedCreditAmount(transaction.getAmount());

            switch (transaction.getStatus()) {
                case FAILED -> usedCredits += usedCreditAmount;
                case SUCCESSFUL -> {
                    usedCredits += usedCreditAmount;
                    successfulCredits += usedCreditAmount;
                }
                default -> {
                }
            }
        }

        return new MonthlyUsage(usedCredits, successfulCredits);
    }

    /**
     * Save updated billing info to the database
     *
     * @param billingInfo The billing info object to save
     * @return The saved copy of the billing info
     */
    public BillingInfo saveBillingInfo(BillingInfo billingInfo) {
        return billingInfoRepository.save(billingInfo);
    }

    /**
     * Attempts to adjust an organization's balance by a certain delta amount,
     * and retries the transaction until it succeeds or a maximum number of tries is reached
     *
     * @param organization The organization to adjust
     * @param balanceDelta The amount to adjust the balance by
     * @param totalUsedDelta The amount to adjust the total used value by
     * @param totalSuccessfulDelta The amount to adjust the total successful value by
     * @return Whether it was successful
     */
    public boolean tryAdjustAccountWithRetries(Organization organization, int balanceDelta,
                                               int totalUsedDelta, int totalSuccessfulDelta) {
        boolean success = false;
        for (int i = 0; i < MAX_ACCOUNT_ADJUSTMENT_RETRIES; ++i) {
            try {
                tryAdjustAccount(organization, balanceDelta, totalUsedDelta, totalSuccessfulDelta);
                success = true;
                break;
            } catch (OptimisticLockException ignored) {
                // This will happen if the balance was modified by another source while we were processing
                // Retry the transaction unless we've hit the max retries
            }
        }
        return success;
    }

    /**
     * Attempts to adjust an organization's balance by a certain delta amount. Throws an exception
     * if a concurrent modification is detected
     *
     * @param organization The organization to adjust
     * @param balanceDelta The amount to adjust the balance by
     * @param totalUsedDelta The amount to adjust the total used value by
     * @param totalSuccessfulDelta The amount to adjust the total successful value by
     * @throws OptimisticLockException If the account balance changed while we were changing it
     */
    public void tryAdjustAccount(Organization organization, int balanceDelta,
                                 int totalUsedDelta, int totalSuccessfulDelta) {
        BillingInfo billingInfo = getBillingInfoForOrg(organization);

        int currentBalance = billingInfo.getBalance();

        // TODO this will allow unlimited/monthly accounts to go into the negative, but
        //      fixing it the right way will take enough work that I'm pushing it to a new PR
        if (isDebit(balanceDelta) && currentBalance < -balanceDelta
            && organization.getPaymentTier() == PaymentTier.AS_NEEDED) {
            throw new InsufficientFundsException(currentBalance, -balanceDelta);
        }

        billingInfo.setBalance(currentBalance + balanceDelta);
        billingInfo.setTotalUsed(billingInfo.getTotalUsed() + totalUsedDelta);
        billingInfo.setTotalSuccessful(billingInfo.getTotalSuccessful() + totalSuccessfulDelta);
        saveBillingInfo(billingInfo);
    }

    private boolean isDebit(int amount) {
        return amount < 0;
    }

    /**
     * Update an organization's payment tier
     *
     * @param organization The organization to update
     * @param paymentTier The new payment tier to give them
     */
    public void updatePaymentTier(Organization organization, PaymentTier paymentTier) {
        // This obviously could be done outside of this function, but I'm putting it in the service
        // in case we need to do more here later
        organization.setPaymentTier(paymentTier);
        organizationService.updateOrganization(organization);
    }

    /**
     * Get the price of a credit
     *
     * @return The price of a credit, in cents
     */
    public long getCreditPrice() {
        return externalBillingService.getCreditPrice();
    }
}
