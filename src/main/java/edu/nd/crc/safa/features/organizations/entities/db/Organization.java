package edu.nd.crc.safa.features.organizations.entities.db;

import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.Lob;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

import edu.nd.crc.safa.features.organizations.entities.app.OrganizationAppEntity;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;

@Entity
@Table(name = "organization")
@Getter
@Setter
@NoArgsConstructor
public class Organization implements IEntityWithMembership {

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
    private String paymentTier;

    @Column
    private boolean personalOrg;

    @Column
    private UUID fullOrgTeamId;

    public Organization(String name, String description, SafaUser owner, String paymentTier, boolean personalOrg) {
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
