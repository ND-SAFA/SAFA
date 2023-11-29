package edu.nd.crc.safa.features.billing.services;

import edu.nd.crc.safa.features.billing.entities.InsufficientFundsException;
import edu.nd.crc.safa.features.billing.entities.db.BillingInfo;
import edu.nd.crc.safa.features.billing.repositories.BillingInfoRepository;
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

    public enum TransactionType {
        CREDIT,
        CHARGE
    }

    /**
     * Apply a transaction to an account
     *
     * @param organization The account to apply the transaction to
     * @param transactionType The type of transaction
     * @param amount The amount of the transaction (always positive)
     */
    @Transactional
    public void transact(Organization organization, TransactionType transactionType, int amount) {
        if (amount < 0) {
            throw new IllegalArgumentException("Amount cannot be negative: " + amount);
        }

        if (amount == 0) {
            throw new IllegalArgumentException("Amount cannot be zero");
        }

        if (transactionType == TransactionType.CHARGE) {
            amount = -amount;
        }

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

        if (!success) {
            throw new SafaError("Unable to adjust account balance, please try again later.");
        }

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
