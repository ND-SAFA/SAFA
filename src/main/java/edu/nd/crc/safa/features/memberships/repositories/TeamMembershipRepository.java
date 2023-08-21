package edu.nd.crc.safa.features.memberships.repositories;

import java.util.UUID;

import edu.nd.crc.safa.features.memberships.entities.db.TeamMembership;

import org.springframework.data.repository.CrudRepository;

public interface TeamMembershipRepository extends CrudRepository<TeamMembership, UUID> {
}
