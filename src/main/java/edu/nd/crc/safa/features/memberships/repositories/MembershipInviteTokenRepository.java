package edu.nd.crc.safa.features.memberships.repositories;

import java.util.UUID;

import edu.nd.crc.safa.features.memberships.entities.db.MembershipInviteToken;

import org.springframework.data.repository.CrudRepository;

public interface MembershipInviteTokenRepository extends CrudRepository<MembershipInviteToken, UUID> {

}
