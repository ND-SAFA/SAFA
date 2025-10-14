package edu.nd.crc.safa.features.organizations.entities.app;

import java.util.UUID;

import edu.nd.crc.safa.features.memberships.entities.db.IEntityMembership;
import edu.nd.crc.safa.features.projects.entities.app.IAppEntity;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class MembershipAppEntity implements IAppEntity {
    private UUID id;
    private String email;
    private String role;
    private MembershipType entityType;
    private UUID entityId;

    /**
     * This constructor is mainly intended for testing
     *
     * @param email The email of the user involved
     * @param role The role to assign them
     */
    public MembershipAppEntity(String email, String role) {
        this.email = email;
        this.role = role;
    }

    public MembershipAppEntity(IEntityMembership membership) {
        this.id = membership.getId();
        this.email = membership.getUser().getEmail();
        this.role = membership.getRole().name();
        this.entityType = membership.getMembershipType();
        this.entityId = membership.getEntity().getId();
    }
}
