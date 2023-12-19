package edu.nd.crc.safa.features.billing.services;

/**
 * Interface for services that handle charging users money
 */
public interface IBillingService {

    // TODO temp interface

    void startTransaction(String referenceId);

    void endTransaction(String referenceId);
}
