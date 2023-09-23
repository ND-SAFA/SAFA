package edu.nd.crc.safa.features.memberships.entities.db;

import java.util.UUID;

import edu.nd.crc.safa.features.organizations.entities.app.MembershipType;

public interface EntityMembership {
    UUID getId();

    String getEmail();

    String getRole();

    MembershipType getMembershipType();

    UUID getEntityId();
}
