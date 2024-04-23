package edu.nd.crc.safa.features.memberships.entities.db;

import java.time.LocalDateTime;
import java.util.UUID;

import edu.nd.crc.safa.features.organizations.entities.db.IEntityWithMembership;
import edu.nd.crc.safa.features.organizations.entities.db.IRole;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.Setter;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;

@Getter
@Setter
@Entity
@Table(name = "membership_invite_token")
public class MembershipInviteToken {

    @Id
    @GeneratedValue
    @JdbcTypeCode(SqlTypes.BINARY)
    @Column
    private UUID id;

    @Column
    @JdbcTypeCode(SqlTypes.BINARY)
    private UUID entityId;

    @Column
    private LocalDateTime expiration;

    @JdbcTypeCode(SqlTypes.VARCHAR)
    @Column
    private String role;

    public MembershipInviteToken(IEntityWithMembership entity, IRole role) {
        this(entity.getId(), role.name());
    }

    public MembershipInviteToken(UUID entityId, String role) {
        this.entityId = entityId;
        this.role = role;
        this.expiration = LocalDateTime.now().plusWeeks(1);
    }

}
