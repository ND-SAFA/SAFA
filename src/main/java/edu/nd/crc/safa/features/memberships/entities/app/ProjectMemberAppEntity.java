package edu.nd.crc.safa.features.memberships.entities.app;

import java.util.UUID;

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
    UUID projectMembershipId;
    String email;
    ProjectRole role;

    public ProjectMemberAppEntity(ProjectMembership projectMembership) {
        this.projectMembershipId = projectMembership.getMembershipId();
        this.email = projectMembership.getMember().getEmail();
        this.role = projectMembership.getRole();
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
