package edu.nd.crc.safa.features.billing.repositories;

import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.billing.entities.db.Transaction;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;

import org.springframework.data.repository.CrudRepository;

public interface TransactionRepository extends CrudRepository<Transaction, UUID> {
    List<Transaction> findByOrganizationAndTimestampIsAfter(Organization organization, LocalDateTime startTime);

    List<Transaction> findByOrganization(Organization organization);
}
