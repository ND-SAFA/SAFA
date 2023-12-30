package edu.nd.crc.safa.features.billing.services;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.billing.entities.app.TransactionAppEntity;
import edu.nd.crc.safa.features.billing.entities.db.Transaction;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;

import org.springframework.stereotype.Service;

@Service
public class BillingService {

    private final CreditBalanceService transactionService;
    private final IExternalBillingService externalBillingService;

    public BillingService(CreditBalanceService transactionService,
                          IExternalBillingService externalBillingService) {
        this.transactionService = transactionService;
        this.externalBillingService = externalBillingService;
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
}
