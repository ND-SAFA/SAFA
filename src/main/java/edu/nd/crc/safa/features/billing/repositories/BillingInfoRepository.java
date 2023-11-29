package edu.nd.crc.safa.features.billing.repositories;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.billing.entities.db.BillingInfo;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;

import org.springframework.data.repository.CrudRepository;

public interface BillingInfoRepository extends CrudRepository<BillingInfo, UUID> {
    Optional<BillingInfo> findByOrganization(Organization organization);
}
