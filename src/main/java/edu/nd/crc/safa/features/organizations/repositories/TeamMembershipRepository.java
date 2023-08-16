package edu.nd.crc.safa.features.organizations.repositories;

import java.util.UUID;

import edu.nd.crc.safa.features.organizations.entities.db.TeamMembership;

import org.springframework.data.repository.CrudRepository;

public interface TeamMembershipRepository extends CrudRepository<TeamMembership, UUID> {
}
