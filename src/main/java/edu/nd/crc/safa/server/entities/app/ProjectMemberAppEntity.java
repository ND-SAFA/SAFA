package edu.nd.crc.safa.server.entities.app;

import edu.nd.crc.safa.server.entities.db.ProjectMembership;
import edu.nd.crc.safa.server.entities.db.ProjectRole;

/**
 * Represents the FEND version of a project member
 */
public class ProjectMemberAppEntity {
    String projectMembershipId;
    String email;
    ProjectRole role;

    public ProjectMemberAppEntity() {

    }

    public ProjectMemberAppEntity(ProjectMembership projectMembership) {
        this.projectMembershipId = projectMembership.getMembershipId().toString();
        this.email = projectMembership.getMember().getEmail();
        this.role = projectMembership.getRole();
    }

    public String getProjectMembershipId() {
        return projectMembershipId;
    }

    public void setProjectMembershipId(String projectMembershipId) {
        this.projectMembershipId = projectMembershipId;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public ProjectRole getRole() {
        return role;
    }

    public void setRole(ProjectRole role) {
        this.role = role;
    }
}
