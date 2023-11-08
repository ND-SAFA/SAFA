package edu.nd.crc.safa.features.memberships.entities.api;

import edu.nd.crc.safa.features.organizations.entities.db.ProjectRole;

import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;

/**
 * The request sent from FEND to request a project membership be added or updated.
 */
public class ProjectMembershipRequest {

    @NotEmpty
    private String memberEmail;

    @NotNull
    private ProjectRole projectRole;

    public ProjectMembershipRequest() {
    }

    public ProjectMembershipRequest(String email, ProjectRole role) {
        this.memberEmail = email;
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
