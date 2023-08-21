package edu.nd.crc.safa.features.memberships.repositories;

import java.util.UUID;

import edu.nd.crc.safa.features.memberships.entities.db.OrganizationMembership;

import org.springframework.data.repository.CrudRepository;

public interface OrganizationMembershipRepository extends CrudRepository<OrganizationMembership, UUID> {
}
