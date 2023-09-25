package edu.nd.crc.safa.features.organizations.entities.app;

import java.util.UUID;

import edu.nd.crc.safa.features.memberships.entities.db.EntityMembership;
import edu.nd.crc.safa.features.projects.entities.app.IAppEntity;

import lombok.Data;

@Data
public class MembershipAppEntity implements IAppEntity {
    private UUID id;
    private String email;
    private String role;
    private MembershipType entityType;
    private UUID entityId;

    public MembershipAppEntity(EntityMembership membership) {
        this.id = membership.getId();
        this.email = membership.getEmail();
        this.role = membership.getRoleAsString();
        this.entityType = membership.getMembershipType();
        this.entityId = membership.getEntityId();

    }
}
