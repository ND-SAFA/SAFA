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

        if (!tryAdjustAccountWithRetries(organization, amount)) {
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
     * @param amount The amount to adjust by
     */
    private boolean tryAdjustAccountWithRetries(Organization organization, int amount) {
        boolean success = false;
        for (int i = 0; i < MAX_TRANSACTION_RETRIES; ++i) {
            try {
                tryAdjustAccount(organization, amount);
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
     * Attempts to adjust an organization's balance by a certain delta amount
     *
     * @param organization The organization to adjust
     * @param delta The amount to adjust by. Can be positive or negative
     */
    private void tryAdjustAccount(Organization organization, int delta) {
        BillingInfo billingInfo = getBillingInfoForOrg(organization);

        int currentBalance = billingInfo.getBalance();

        if (delta < 0 && currentBalance < -delta) {
            throw new InsufficientFundsException(currentBalance, -delta);
        }

        billingInfo.setBalance(currentBalance + delta);
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
        Transaction.Status status = transaction.getStatus();

        if (status != Transaction.Status.PENDING) {
            throw new IllegalArgumentException("Cannot mark a finished transaction as failed.");
        }

        if (!wasReversed(transaction)) {
            reverseTransaction(transaction);
        }

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
        if (wasReversed(transaction)) {
            throw new IllegalArgumentException("Cannot mark transaction as successful as it was already reversed.");
        }

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
        if (!wasReversed(transaction)) {
            reverseTransaction(transaction);
        }

        transaction.setStatus(Transaction.Status.REFUNDED);
        return transactionRepository.save(transaction);
    }

    /**
     * Returns whether the given transaction was reversed
     *
     * @param transaction The transaction
     * @return Whether the transaction was reversed
     */
    private boolean wasReversed(Transaction transaction) {
        Transaction.Status status = transaction.getStatus();
        return status == Transaction.Status.FAILED || status == Transaction.Status.REFUNDED;
    }

    /**
     * Reverses a transaction. Applies the negative of the transaction amount to the balance
     * of the organization the transaction belongs to
     *
     * @param transaction The transaction to reverse
     */
    private void reverseTransaction(Transaction transaction) {
        boolean success = tryAdjustAccountWithRetries(transaction.getOrganization(), -transaction.getAmount());

        if (!success) {
            throw new SafaError("Failed to refund transaction with ID " + transaction.getId());
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
                return billingInfoRepository.save(billingInfo);
            });
    }
}
