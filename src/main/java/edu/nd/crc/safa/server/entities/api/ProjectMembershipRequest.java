package edu.nd.crc.safa.server.entities.api;

import java.util.UUID;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectRole;
import edu.nd.crc.safa.server.entities.db.SafaUser;

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

    public ProjectMembershipRequest(Project project, SafaUser member, ProjectRole role) {
        this.projectId = project.getProjectId();
        this.memberEmail = member.getEmail();
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
