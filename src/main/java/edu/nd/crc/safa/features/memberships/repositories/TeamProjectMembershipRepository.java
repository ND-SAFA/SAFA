package edu.nd.crc.safa.features.memberships.repositories;

import java.util.UUID;

import edu.nd.crc.safa.features.memberships.entities.db.TeamProjectMembership;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TeamProjectMembershipRepository extends CrudRepository<TeamProjectMembership, UUID> {
}
