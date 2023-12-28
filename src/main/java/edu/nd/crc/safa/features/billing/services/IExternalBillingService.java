package edu.nd.crc.safa.features.billing.services;

/**
 * Interface for services that handle charging users money
 */
public interface IExternalBillingService {

    /**
     * Begin a transaction with the external interface
     *
     * @param referenceId Some string to reference the transaction
     * @param amount The amount of the transaction
     * @return The url to redirect to in order to complete the transaction
     */
    String startTransaction(String referenceId, int amount);

    /**
     * Complete a transaction with the external interface
     *
     * @param referenceId The same string for the transaction that was passed into
     *                    {@link #startTransaction(String, int)}
     */
    void endTransaction(String referenceId);
}
