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
public class Organization {

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
}
