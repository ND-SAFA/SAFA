package edu.nd.crc.safa.features.memberships.entities.db;

import java.util.UUID;

import edu.nd.crc.safa.features.organizations.entities.app.MembershipType;
import edu.nd.crc.safa.features.organizations.entities.db.IEntityWithMembership;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.OrganizationRole;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.type.SqlTypes;

@Entity
@Table(name = "org_membership")
@Getter
@Setter
@NoArgsConstructor
public class OrganizationMembership implements IEntityMembership {

    @Id
    @JdbcTypeCode(SqlTypes.BINARY)
    @GeneratedValue
    @Column
    private UUID id;

    @JoinColumn(name = "user_id")
    @OnDelete(action = OnDeleteAction.CASCADE)
    @ManyToOne
    private SafaUser user;

    @JdbcTypeCode(SqlTypes.BINARY)
    @JoinColumn(name = "org_id")
    @OnDelete(action = OnDeleteAction.CASCADE)
    @ManyToOne
    private Organization organization;

    @Enumerated(EnumType.STRING)
    @JdbcTypeCode(SqlTypes.VARCHAR)
    @Column
    private OrganizationRole role;

    public OrganizationMembership(SafaUser user, Organization organization, OrganizationRole role) {
        this.user = user;
        this.organization = organization;
        this.role = role;
    }

    @Override
    public MembershipType getMembershipType() {
        return MembershipType.ORGANIZATION;
    }

    @Override
    public IEntityWithMembership getEntity() {
        return organization;
    }
}
