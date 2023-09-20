package edu.nd.crc.safa.features.memberships.entities.app;

import java.util.UUID;

import edu.nd.crc.safa.features.memberships.entities.db.TeamMembership;
import edu.nd.crc.safa.features.memberships.entities.db.UserProjectMembership;
import edu.nd.crc.safa.features.organizations.entities.db.ProjectRole;
import edu.nd.crc.safa.features.organizations.entities.db.TeamRole;
import edu.nd.crc.safa.features.projects.entities.app.IAppEntity;

import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Represents the FEND version of a project member
 */
@NoArgsConstructor
@Data
public class ProjectMemberAppEntity implements IAppEntity {
    private UUID id;
    private String email;
    private ProjectRole role;

    public ProjectMemberAppEntity(UserProjectMembership projectMembership) {
        this.id = projectMembership.getMembershipId();
        this.email = projectMembership.getMember().getEmail();
        this.role = projectMembership.getRole();
    }

    // TODO update this all to new api once that's fleshed out and also fix the roles
    public ProjectMemberAppEntity(TeamMembership teamMembership) {
        this.id = teamMembership.getId();
        this.email = teamMembership.getUser().getEmail();
        try {
            if (teamMembership.getRole() == TeamRole.ADMIN) {
                this.role = ProjectRole.OWNER;
            } else {
                this.role = Enum.valueOf(ProjectRole.class, teamMembership.getRole().name());
            }
        } catch (IllegalArgumentException ignored) {
            this.role = ProjectRole.NONE;
        }

    }
}
