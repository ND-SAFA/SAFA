package edu.nd.crc.safa.features.billing.services;

import edu.nd.crc.safa.features.billing.entities.db.Transaction;

/**
 * Interface for services that handle charging users money
 */
public interface IExternalBillingService {

    /**
     * Begin a transaction with the external interface. This is called
     * after the transaction has been created on our end, and is used to
     * actually initiate the billing process.
     *
     * @param transaction The transaction to apply
     * @return The url to redirect to in order to complete the transaction
     */
    String startTransaction(Transaction transaction);

    /**
     * Complete a transaction with the external interface. This is called
     * after the transaction is marked completed on our end, and is used to
     * do any cleanup needed for finished transactions such as confirming
     * fulfillment.
     *
     * @param transaction The transaction that is ending
     */
    void endTransaction(Transaction transaction);

    /**
     * Cancel a transaction with the external interface. This is called
     * after the transaction is marked canceled on our end, and is used to
     * clean up any open billing sessions that may be remaining.
     *
     * @param transaction The transaction that is being canceled
     */
    void cancelTransaction(Transaction transaction);

    /**
     * Get the price of a single credit, in cents
     *
     * @return The price of a credit, in cents
     */
    long getCreditPrice();
}
