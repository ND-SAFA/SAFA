package edu.nd.crc.safa.features.memberships.entities.app;

import edu.nd.crc.safa.features.memberships.entities.db.ProjectMembership;
import edu.nd.crc.safa.features.projects.entities.app.IAppEntity;
import edu.nd.crc.safa.features.users.entities.db.ProjectRole;

import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Represents the FEND version of a project member
 */
@NoArgsConstructor
@Data
public class ProjectMemberAppEntity implements IAppEntity {
    String projectMembershipId;
    String email;
    ProjectRole role;

    public ProjectMemberAppEntity(ProjectMembership projectMembership) {
        this.projectMembershipId = projectMembership.getMembershipId().toString();
        this.email = projectMembership.getMember().getEmail();
        this.role = projectMembership.getRole();
    }

    @Override
    public String getBaseEntityId() {
        return this.projectMembershipId;
    }

    @Override
    public void setBaseEntityId(String id) {
        this.projectMembershipId = id;
    }
}
