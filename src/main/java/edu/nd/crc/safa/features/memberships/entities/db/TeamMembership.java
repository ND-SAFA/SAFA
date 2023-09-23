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
import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.organizations.entities.db.TeamRole;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;

@Entity
@Table(name = "team_membership")
@Getter
@Setter
@NoArgsConstructor
public class TeamMembership implements EntityMembership {

    @Id
    @GeneratedValue
    @Column
    private UUID id;

    @JoinColumn(name = "user_id")
    @OnDelete(action = OnDeleteAction.CASCADE)
    @ManyToOne
    private SafaUser user;

    @JoinColumn(name = "team_id")
    @OnDelete(action = OnDeleteAction.CASCADE)
    @ManyToOne
    private Team team;

    @Column
    @Enumerated(EnumType.STRING)
    private TeamRole role;

    public TeamMembership(SafaUser user, Team team, TeamRole role) {
        this.user = user;
        this.team = team;
        this.role = role;
    }

    @Override
    public String getEmail() {
        return user.getEmail();
    }

    @Override
    public MembershipType getMembershipType() {
        return MembershipType.TEAM;
    }

    @Override
    public UUID getEntityId() {
        return team.getId();
    }
}
