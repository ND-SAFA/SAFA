package edu.nd.crc.safa.features.organizations.entities.db;

import java.util.UUID;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
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
@Table(name = "team")
@Getter
@Setter
@NoArgsConstructor
public class Team {

    @Id
    @JdbcTypeCode(SqlTypes.BINARY)
    @GeneratedValue
    @Column
    private UUID id;

    @Column
    private String name;

    @JoinColumn(name = "organization_id")
    @OnDelete(action = OnDeleteAction.CASCADE)
    @ManyToOne
    private Organization organization;

    @Column
    private boolean fullOrgTeam;

    public Team(String name, Organization organization, boolean fullOrgTeam) {
        this.name = name;
        this.organization = organization;
        this.fullOrgTeam = fullOrgTeam;
    }

}
