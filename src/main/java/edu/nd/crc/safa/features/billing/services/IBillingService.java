package edu.nd.crc.safa.features.billing.services;

/**
 * Interface for services that handle charging users money
 */
public interface IBillingService {

    // TODO temp interface

    /**
     *
     * @param referenceId Some string to reference the transaction
     * @return The url to redirect to TODO this might not be the most reusable interface
     */
    String startTransaction(String referenceId);

    void endTransaction(String referenceId);
}
