package edu.nd.crc.safa.features.billing.services;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.billing.entities.db.Transaction;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;

import org.springframework.stereotype.Service;

@Service
public class BillingService {

    private final BalanceTransactionService transactionService;
    private final IExternalBillingService externalBillingService;

    public BillingService(BalanceTransactionService transactionService,
                          IExternalBillingService externalBillingService) {
        this.transactionService = transactionService;
        this.externalBillingService = externalBillingService;
    }

    public String startTransaction(Organization organization, int amount, String description) {
        Transaction transaction = null;
        
        try {
            transaction = transactionService.credit(organization, amount, description);
            return externalBillingService.startTransaction(transaction.getId().toString(), amount);
        } catch (Exception e) {
            if (transaction != null) {
                transactionService.markTransactionFailed(transaction);
            }
            throw e;
        }
    }

    public void endTransaction(String referenceId) {
        UUID transactionId = UUID.fromString(referenceId);
        Optional<Transaction> transactionOptional = transactionService.getTransactionOptionalById(transactionId);

        if (transactionOptional.isPresent()) {
            Transaction transaction = transactionOptional.get();
            transactionService.markTransactionSuccessful(transaction);
            externalBillingService.endTransaction(referenceId);
        }
    }
}
