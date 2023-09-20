package edu.nd.crc.safa.features.organizations.entities.app;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.projects.entities.app.ProjectIdAppEntity;

import lombok.Data;

@Data
public class TeamAppEntity {
    private UUID id;
    private String name;
    private List<MembershipAppEntity> members;
    private List<ProjectIdAppEntity> projects;

    public TeamAppEntity(Team team, List<MembershipAppEntity> members, List<ProjectIdAppEntity> projects) {
        this.id = team.getId();
        this.name = team.getName();
        this.members = members;
        this.projects = projects;
    }
}
