package edu.nd.crc.safa.features.billing.services;

import edu.nd.crc.safa.features.billing.entities.InsufficientFundsException;
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

@Service
@RequiredArgsConstructor
public class BillingService {

    private static final int MAX_TRANSACTION_RETRIES = 5;

    private final BillingInfoRepository billingInfoRepository;
    private final TransactionRepository transactionRepository;

    /**
     * Apply a transaction to an account. Make sure to update the
     * status of the transaction with the markTransaction* functions
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

        if (!tryAdjustAccountWithRetries(organization, amount, 0, 0)) {
            throw new SafaError("Unable to adjust account balance, please try again later.");
        }

        Transaction transaction = new Transaction(amount, description, organization);
        return transactionRepository.save(transaction);
    }

    /**
     * Attempts to adjust an organization's balance by a certain delta amount,
     * and retries the transaction until it succeeds or a maximum number of tries is reached
     *
     * @param organization The organization to adjust
     * @param balanceAmount The amount to adjust the balance by
     * @param totalUsedAmount The amount to adjust the total used value by
     * @param totalSuccessfulAmount The amount to adjust the total successful value by
     * @return Whether it was successful
     */
    private boolean tryAdjustAccountWithRetries(Organization organization, int balanceAmount,
                                                int totalUsedAmount, int totalSuccessfulAmount) {
        boolean success = false;
        for (int i = 0; i < MAX_TRANSACTION_RETRIES; ++i) {
            try {
                tryAdjustAccount(organization, balanceAmount, totalUsedAmount, totalSuccessfulAmount);
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
     * @param balanceAmount The amount to adjust the balance by
     * @param totalUsedAmount The amount to adjust the total used value by
     * @param totalSuccessfulAmount The amount to adjust the total successful value by
     */
    private void tryAdjustAccountForTransaction(Transaction transaction, int balanceAmount,
                                                   int totalUsedAmount, int totalSuccessfulAmount) {
        boolean success = tryAdjustAccountWithRetries(transaction.getOrganization(), balanceAmount,
            totalUsedAmount, totalSuccessfulAmount);
        if (!success) {
            throw new SafaError("Failed to refund transaction with ID " + transaction.getId());
        }
    }

    /**
     * Attempts to adjust an organization's balance by a certain delta amount
     *
     * @param organization The organization to adjust
     * @param balanceAmount The amount to adjust the balance by
     * @param totalUsedAmount The amount to adjust the total used value by
     * @param totalSuccessfulAmount The amount to adjust the total successful value by
     */
    private void tryAdjustAccount(Organization organization, int balanceAmount,
                                  int totalUsedAmount, int totalSuccessfulAmount) {
        BillingInfo billingInfo = getBillingInfoForOrg(organization);

        int currentBalance = billingInfo.getBalance();

        if (balanceAmount < 0 && currentBalance < -balanceAmount) {
            throw new InsufficientFundsException(currentBalance, -balanceAmount);
        }

        billingInfo.setBalance(currentBalance + balanceAmount);
        billingInfo.setTotalUsed(billingInfo.getTotalUsed() + totalUsedAmount);
        billingInfo.setTotalSuccessful(billingInfo.getTotalSuccessful() + totalSuccessfulAmount);
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

        tryAdjustAccountForTransaction(transaction, -amount, toUsedCreditAmount(amount), 0);

        transaction.setStatus(Transaction.Status.FAILED);
        return transactionRepository.save(transaction);
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

        tryAdjustAccountForTransaction(transaction, 0, toUsedCreditAmount(amount), toUsedCreditAmount(amount));

        transaction.setStatus(Transaction.Status.SUCCESSFUL);
        return transactionRepository.save(transaction);
    }

    /**
     * Mark a transaction as refunded and return the funds to the account (if not already done)
     *
     * @param transaction The transaction to mark refunded
     * @return The updated transaction
     */
    public Transaction markTransactionRefunded(Transaction transaction) {
        Transaction.Status status = transaction.getStatus();
        int amount = transaction.getAmount();

        switch (status) {
            case FAILED -> tryAdjustAccountForTransaction(transaction, 0, -toUsedCreditAmount(amount), 0);
            case PENDING -> tryAdjustAccountForTransaction(transaction, -amount, 0, 0);
            case SUCCESSFUL -> tryAdjustAccountForTransaction(transaction, -amount, -toUsedCreditAmount(amount),
                                                                -toUsedCreditAmount(amount));
            default -> {
            }
        }

        transaction.setStatus(Transaction.Status.REFUNDED);
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
        if (transactionAmount < 0) {
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
}
