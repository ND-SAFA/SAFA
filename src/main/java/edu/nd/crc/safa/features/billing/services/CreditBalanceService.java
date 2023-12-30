package edu.nd.crc.safa.features.billing.services;

import java.time.LocalDateTime;
import java.time.temporal.ChronoField;
import java.time.temporal.TemporalAdjusters;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.billing.entities.InsufficientFundsException;
import edu.nd.crc.safa.features.billing.entities.MonthlyUsage;
import edu.nd.crc.safa.features.billing.entities.db.BillingInfo;
import edu.nd.crc.safa.features.billing.entities.db.Transaction;
import edu.nd.crc.safa.features.billing.repositories.BillingInfoRepository;
import edu.nd.crc.safa.features.billing.repositories.TransactionRepository;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;

import jakarta.persistence.OptimisticLockException;
import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

/**
 * This service updates organization balances and tracks
 * the transactions that caused the updates. It does not handle
 * any actual money, just the credits that are tied to the
 * organization.
 */
@Service
@RequiredArgsConstructor
public class CreditBalanceService {

    private static final int MAX_TRANSACTION_RETRIES = 5;

    private final BillingInfoRepository billingInfoRepository;
    private final TransactionRepository transactionRepository;

    public Optional<Transaction> getTransactionOptionalById(UUID id) {
        return transactionRepository.findById(id);
    }

    /**
     * Apply a transaction to an account. The transaction will be in the PENDING
     * state. Make sure to update the status of the transaction with the
     * markTransaction* functions.<br>
     * <br>
     * If the transaction is a charge (i.e. the amount is negative), adjust the
     * balance of the account immediately. If the transaction is a credit
     * (i.e. the amount is positive), wait to adjust the balance until the
     * transaction is marked successful.
     *
     * @param organization The account to apply the transaction to
     * @param amount The amount of the transaction
     * @param description The description of the transaction
     * @return The db entity for this transaction
     */
    private Transaction transact(Organization organization, int amount, String description) {
        if (amount == 0) {
            throw new IllegalArgumentException("Amount cannot be zero");
        }

        if (isDebit(amount)) {
            if (!tryAdjustAccountWithRetries(organization, amount, 0, 0)) {
                throw new SafaError("Unable to adjust account balance, please try again later.");
            }
        }

        Transaction transaction = new Transaction(amount, description, organization);
        return saveTransaction(transaction);
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
    private boolean tryAdjustAccountWithRetries(Organization organization, int balanceDelta,
                                                int totalUsedDelta, int totalSuccessfulDelta) {
        boolean success = false;
        for (int i = 0; i < MAX_TRANSACTION_RETRIES; ++i) {
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
     * Attempts to adjust an organization's balance by a certain delta amount,
     * and retries the transaction until it succeeds or a maximum number of tries is reached
     *
     * @param transaction The transaction to adjust amounts for
     * @param balanceDelta The amount to adjust the balance by
     * @param totalUsedDelta The amount to adjust the total used value by
     * @param totalSuccessfulDelta The amount to adjust the total successful value by
     */
    private void tryAdjustAccountForTransaction(Transaction transaction, int balanceDelta,
                                                int totalUsedDelta, int totalSuccessfulDelta) {
        boolean success = tryAdjustAccountWithRetries(transaction.getOrganization(), balanceDelta,
            totalUsedDelta, totalSuccessfulDelta);
        if (!success) {
            throw new SafaError("Failed to adjust transaction with ID " + transaction.getId());
        }
    }

    /**
     * Attempts to adjust an organization's balance by a certain delta amount
     *
     * @param organization The organization to adjust
     * @param balanceDelta The amount to adjust the balance by
     * @param totalUsedDelta The amount to adjust the total used value by
     * @param totalSuccessfulDelta The amount to adjust the total successful value by
     */
    private void tryAdjustAccount(Organization organization, int balanceDelta,
                                  int totalUsedDelta, int totalSuccessfulDelta) {
        BillingInfo billingInfo = getBillingInfoForOrg(organization);

        int currentBalance = billingInfo.getBalance();

        if (isDebit(balanceDelta) && currentBalance < -balanceDelta) {
            throw new InsufficientFundsException(currentBalance, -balanceDelta);
        }

        billingInfo.setBalance(currentBalance + balanceDelta);
        billingInfo.setTotalUsed(billingInfo.getTotalUsed() + totalUsedDelta);
        billingInfo.setTotalSuccessful(billingInfo.getTotalSuccessful() + totalSuccessfulDelta);
        billingInfoRepository.save(billingInfo);
    }

    /**
     * Charge an account a certain amount
     *
     * @param organization The account to charge
     * @param amount The amount to charge
     * @param description The description of the transaction
     * @return The db entity for this transaction
     */
    @Transactional
    public Transaction charge(Organization organization, int amount, String description) {
        if (amount < 0) {
            throw new IllegalArgumentException("Amount cannot be negative: " + amount);
        }
        return transact(organization, -amount, description);
    }

    /**
     * Credit an account a certain amount
     *
     * @param organization The account to credit
     * @param amount The amount to credit
     * @param description The description of the transaction
     * @return The db entity for this transaction
     */
    @Transactional
    public Transaction credit(Organization organization, int amount, String description) {
        if (amount < 0) {
            throw new IllegalArgumentException("Amount cannot be negative: " + amount);
        }
        return transact(organization, amount, description);
    }

    private boolean isCredit(int amount) {
        return amount > 0;
    }

    private boolean isDebit(int amount) {
        return amount < 0;
    }

    /**
     * Mark a transaction as failed. This will fail if the transaction already finished.
     *
     * @param transaction The transaction to mark failed
     * @return The updated transaction
     */
    public Transaction markTransactionFailed(Transaction transaction) {
        int amount = transaction.getAmount();

        if (transaction.getStatus() != Transaction.Status.PENDING) {
            throw new IllegalArgumentException("Cannot mark a finished transaction as failed.");
        }

        int balanceAdjustment = 0;
        if (isDebit(amount)) {
            balanceAdjustment = -amount;
        }

        tryAdjustAccountForTransaction(transaction, balanceAdjustment, toUsedCreditAmount(amount), 0);

        transaction.setStatus(Transaction.Status.FAILED);
        return saveTransaction(transaction);
    }

    /**
     * Mark a transaction as successful. This will fail if the transaction was reversed previously.
     *
     * @param transaction The transaction to mark successful
     * @return The updated transaction
     */
    public Transaction markTransactionSuccessful(Transaction transaction) {
        int amount = transaction.getAmount();

        if (transaction.getStatus() != Transaction.Status.PENDING) {
            throw new IllegalArgumentException("Cannot mark a finished transaction as successful.");
        }

        int balanceAdjustment = 0;
        if (isCredit(amount)) {
            balanceAdjustment = amount;
        }

        int usedCreditAmount = toUsedCreditAmount(amount);

        tryAdjustAccountForTransaction(transaction, balanceAdjustment, usedCreditAmount, usedCreditAmount);

        transaction.setStatus(Transaction.Status.SUCCESSFUL);
        return saveTransaction(transaction);
    }

    /**
     * Mark a transaction as canceled and return the funds to the account (if not already done)
     *
     * @param transaction The transaction to mark canceled
     * @return The updated transaction
     */
    public Transaction markTransactionCanceled(Transaction transaction) {
        Transaction.Status status = transaction.getStatus();
        int amount = transaction.getAmount();

        int usedCreditAmount = toUsedCreditAmount(amount);

        int debitAmount = 0;
        if (isDebit(amount)) {
            debitAmount = amount;
        }

        switch (status) {
            case FAILED ->
                tryAdjustAccountForTransaction(transaction, 0, -usedCreditAmount, 0);
            case PENDING ->
                tryAdjustAccountForTransaction(transaction, -debitAmount, 0, 0);
            case SUCCESSFUL ->
                tryAdjustAccountForTransaction(transaction, -amount, -usedCreditAmount, -usedCreditAmount);
            default -> {
            }
        }

        transaction.setStatus(Transaction.Status.CANCELED);
        return saveTransaction(transaction);
    }

    /**
     * Saves a transaction object to the database and returns the saved copy
     *
     * @param transaction The transaction to save
     * @return The saved copy of the transaction
     */
    public Transaction saveTransaction(Transaction transaction) {
        return transactionRepository.save(transaction);
    }

    /**
     * Determines the used credit amount for a transaction based on the
     * transaction's amount. If the transaction is a credit (transactionAmount
     * is greater than 0), this function returns 0 since no credits are
     * used when they're being given to an account. If the transaction is
     * a charge (transactionAmount is less than 0), the function returns
     * the transactionAmount negated since the number of credits being used
     * is the positive value of the negative charge.
     *
     * @param transactionAmount The amount of the transaction
     * @return How many credits were used by this transaction
     */
    private int toUsedCreditAmount(int transactionAmount) {
        if (isDebit(transactionAmount)) {
            return -transactionAmount;
        }
        return 0;
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
                return billingInfoRepository.save(billingInfo);
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
        List<Transaction> thisMonthTransactions =
            transactionRepository.findByOrganizationAndTimestampIsAfter(organization, monthStart);

        int usedCredits = 0;
        int successfulCredits = 0;

        for (Transaction transaction : thisMonthTransactions) {
            int usedCreditAmount = toUsedCreditAmount(transaction.getAmount());

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
}
