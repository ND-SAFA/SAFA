package edu.nd.crc.safa.features.organizations.entities.db;

import java.util.UUID;

import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.Lob;
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
@Table(name = "organization")
@Getter
@Setter
@NoArgsConstructor
public class Organization {
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
    private String paymentTier;

    @Column
    private boolean personalOrg;
    
    @JdbcTypeCode(SqlTypes.BINARY)
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
