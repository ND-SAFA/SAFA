package edu.nd.crc.safa.server.entities.api;

import java.util.UUID;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.server.entities.db.ProjectRole;

/**
 * The request sent from FEND to request a project membership be added or updated.
 */
public class ProjectMembershipRequest {

    @NotEmpty
    UUID projectId;

    @NotEmpty
    String memberEmail;

    @NotNull
    ProjectRole projectRole;

    public ProjectMembershipRequest() {
    }

    public ProjectMembershipRequest(UUID projectId, String email, ProjectRole role) {
        this.projectId = projectId;
        this.memberEmail = email;
        this.projectRole = role;
    }

    public UUID getProjectId() {
        return projectId;
    }

    public void setProjectId(UUID projectId) {
        this.projectId = projectId;
    }

    public String getMemberEmail() {
        return memberEmail;
    }

    public void setMemberEmail(String memberEmail) {
        this.memberEmail = memberEmail;
    }

    public ProjectRole getProjectRole() {
        return projectRole;
    }

    public void setProjectRole(ProjectRole projectRole) {
        this.projectRole = projectRole;
    }
}
