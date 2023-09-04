package edu.nd.crc.safa.features.organizations.repositories;

import java.util.UUID;

import edu.nd.crc.safa.features.organizations.entities.db.Organization;

import org.springframework.data.repository.CrudRepository;

public interface OrganizationRepository extends CrudRepository<Organization, UUID> {
}
