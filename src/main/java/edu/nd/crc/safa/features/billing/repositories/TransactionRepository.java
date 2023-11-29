package edu.nd.crc.safa.features.billing.repositories;

import java.util.UUID;

import edu.nd.crc.safa.features.billing.entities.db.Transaction;

import org.springframework.data.repository.CrudRepository;

public interface TransactionRepository extends CrudRepository<Transaction, UUID> {
}
