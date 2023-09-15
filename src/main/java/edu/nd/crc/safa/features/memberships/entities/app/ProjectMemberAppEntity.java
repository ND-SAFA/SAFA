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
    UUID projectMembershipId;
    String email;
    ProjectRole role;

    public ProjectMemberAppEntity(UserProjectMembership projectMembership) {
        this.projectMembershipId = projectMembership.getMembershipId();
        this.email = projectMembership.getMember().getEmail();
        this.role = projectMembership.getRole();
    }

    // TODO update this all to new api once that's fleshed out and also fix the roles
    public ProjectMemberAppEntity(TeamMembership teamMembership) {
        this.projectMembershipId = teamMembership.getId();
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

    @Override
    public UUID getId() {
        return this.projectMembershipId;
    }

    @Override
    public void setId(UUID id) {
        this.projectMembershipId = id;
    }
}
