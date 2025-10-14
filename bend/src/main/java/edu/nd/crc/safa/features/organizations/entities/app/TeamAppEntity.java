package edu.nd.crc.safa.features.organizations.entities.app;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.projects.entities.app.ProjectIdAppEntity;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class TeamAppEntity {
    private UUID id;
    private String name;
    private List<MembershipAppEntity> members;
    private List<ProjectIdAppEntity> projects;
    private List<String> permissions;

    /**
     * This constructor sets the fields that are read by our creation/modification endpoints.
     * It should only be used for testing
     *
     * @param name The name of the team
     */
    public TeamAppEntity(String name) {
        this.name = name;
    }

    public TeamAppEntity(Team team, List<MembershipAppEntity> members,
                         List<ProjectIdAppEntity> projects,List<String> permissions) {
        this.id = team.getId();
        this.name = team.getName();
        this.members = members;
        this.projects = projects;
        this.permissions = permissions;
    }
}
