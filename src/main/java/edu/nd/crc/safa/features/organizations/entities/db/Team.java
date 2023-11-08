package edu.nd.crc.safa.features.organizations.entities.db;

import java.util.UUID;

import edu.nd.crc.safa.features.organizations.entities.app.TeamAppEntity;

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
public class Team implements IEntityWithMembership {

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

    /**
     * Set values using an {@link TeamAppEntity} as a template. This allows us to control
     * which values the front end can tell us to update. We also check each value to see if its null
     * so that the front end doesn't have to send every value every time.
     *
     * @param teamAppEntity The values that need to be updated
     */
    public void setFromAppEntity(TeamAppEntity teamAppEntity) {
        if (teamAppEntity.getName() != null) {
            setName(teamAppEntity.getName());
        }
    }
}
