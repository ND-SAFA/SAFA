package edu.nd.crc.safa.features.memberships.entities.db;

import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

import edu.nd.crc.safa.features.organizations.entities.app.MembershipType;
import edu.nd.crc.safa.features.organizations.entities.db.ProjectRole;
import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.projects.entities.db.Project;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;

@Entity
@Table(name = "team_project_membership")
@Getter
@Setter
@NoArgsConstructor
public class TeamProjectMembership implements EntityMembership {

    @Id
    @GeneratedValue
    @Column
    private UUID id;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "project_id")
    private Project project;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "team_id")
    private Team team;

    public TeamProjectMembership(Project project, Team team) {
        this.project = project;
        this.team = team;
    }

    @Override
    public String getEmail() {
        return null;
    }

    @Override
    public String getRole() {
        return ProjectRole.VIEWER.name();
    }

    @Override
    public MembershipType getMembershipType() {
        return MembershipType.PROJECT;
    }

    @Override
    public UUID getEntityId() {
        return project.getProjectId();
    }
}
