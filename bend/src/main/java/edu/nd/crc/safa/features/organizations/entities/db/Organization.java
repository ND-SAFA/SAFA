package edu.nd.crc.safa.features.organizations.entities.db;

import java.util.UUID;

import edu.nd.crc.safa.features.organizations.entities.app.OrganizationAppEntity;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.Lob;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.hibernate.annotations.JdbcType;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.type.SqlTypes;
import org.hibernate.type.descriptor.jdbc.VarcharJdbcType;

@Entity
@Table(name = "organization")
@Getter
@Setter
@NoArgsConstructor
public class Organization implements IEntityWithMembership {
    @JdbcTypeCode(SqlTypes.BINARY)
    @Id
    @GeneratedValue
    @Column
    private UUID id;

    @Column
    private String name;

    @Column(columnDefinition = "mediumtext")
    @Lob
    private String description;

    @JoinColumn(name = "owner_id")
    @OnDelete(action = OnDeleteAction.CASCADE)
    @ManyToOne
    private SafaUser owner;

    @Column
    @Enumerated(EnumType.STRING)
    @JdbcType(VarcharJdbcType.class)
    private PaymentTier paymentTier;

    @Column
    private boolean personalOrg;
    
    @JdbcTypeCode(SqlTypes.BINARY)
    @Column
    private UUID fullOrgTeamId;

    public Organization(String name, String description, SafaUser owner, PaymentTier paymentTier, boolean personalOrg) {
        this.name = name;
        this.description = description;
        this.owner = owner;
        this.paymentTier = paymentTier;
        this.personalOrg = personalOrg;
    }

    /**
     * Set values using an {@link OrganizationAppEntity} as a template. This allows us to control
     * which values the front end can tell us to update. We also check each value to see if its null
     * so that the front end doesn't have to send every value every time.
     *
     * @param appEntity The values that need to be updated
     */
    public void setFromAppEntity(OrganizationAppEntity appEntity) {
        if (appEntity.getName() != null) {
            setName(appEntity.getName());
        }

        if (appEntity.getDescription() != null) {
            setDescription(appEntity.getDescription());
        }
    }
}
