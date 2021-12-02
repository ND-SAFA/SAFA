package edu.nd.crc.safa.server.entities.api;

import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.server.entities.db.ProjectRole;
import edu.nd.crc.safa.server.entities.db.SafaUser;

/**
 * The request sent from FEND to request a project membership be added or updated.
 */
public class ProjectMembershipRequest {

    @NotEmpty
    String memberEmail;

    @NotNull
    ProjectRole projectRole;

    public ProjectMembershipRequest() {
    }

    public ProjectMembershipRequest(SafaUser member, ProjectRole role) {
        this.memberEmail = member.getEmail();
        this.projectRole = role;
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
