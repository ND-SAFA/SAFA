package edu.nd.crc.safa.features.memberships.entities.db;

import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.EnumType;
import javax.persistence.Enumerated;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

import edu.nd.crc.safa.features.organizations.entities.app.MembershipType;
import edu.nd.crc.safa.features.organizations.entities.db.IEntityWithMembership;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.OrganizationRole;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;

@Entity
@Table(name = "org_membership")
@Getter
@Setter
@NoArgsConstructor
public class OrganizationMembership implements IEntityMembership {

    @Id
    @GeneratedValue
    @Column
    private UUID id;

    @JoinColumn(name = "user_id")
    @OnDelete(action = OnDeleteAction.CASCADE)
    @ManyToOne
    private SafaUser user;

    @JoinColumn(name = "org_id")
    @OnDelete(action = OnDeleteAction.CASCADE)
    @ManyToOne
    private Organization organization;

    @Column
    @Enumerated(EnumType.STRING)
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
