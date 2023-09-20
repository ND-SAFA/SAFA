package edu.nd.crc.safa.features.organizations.entities.app;

import java.util.UUID;

import edu.nd.crc.safa.features.memberships.entities.db.OrganizationMembership;
import edu.nd.crc.safa.features.memberships.entities.db.TeamMembership;
import edu.nd.crc.safa.features.memberships.entities.db.TeamProjectMembership;
import edu.nd.crc.safa.features.memberships.entities.db.UserProjectMembership;
import edu.nd.crc.safa.features.organizations.entities.db.ProjectRole;
import edu.nd.crc.safa.features.projects.entities.app.IAppEntity;

import lombok.Data;

@Data
public class MembershipAppEntity implements IAppEntity {
    private UUID id;
    private String email;
    private String role;
    private MembershipType entityType;
    private UUID entityId;

    public MembershipAppEntity(OrganizationMembership organizationMembership) {
        this.id = organizationMembership.getId();
        this.email = organizationMembership.getUser().getEmail();
        this.role = organizationMembership.getRole().name();
        this.entityType = MembershipType.ORGANIZATION;
        this.entityId = organizationMembership.getOrganization().getId();
    }

    public MembershipAppEntity(TeamMembership teamMembership) {
        this.id = teamMembership.getId();
        this.email = teamMembership.getUser().getEmail();
        this.role = teamMembership.getRole().name();
        this.entityType = MembershipType.TEAM;
        this.entityId = teamMembership.getTeam().getId();
    }

    public MembershipAppEntity(UserProjectMembership userProjectMembership) {
        this.id = userProjectMembership.getMembershipId();
        this.email = userProjectMembership.getMember().getEmail();
        this.role = userProjectMembership.getRole().name();
        this.entityType = MembershipType.PROJECT;
        this.entityId = userProjectMembership.getProject().getProjectId();
    }

    public MembershipAppEntity(TeamProjectMembership teamProjectMembership) {
        this.id = teamProjectMembership.getId();
        this.email = null;
        this.role = ProjectRole.VIEWER.name();
        this.entityType = MembershipType.PROJECT;
        this.entityId = teamProjectMembership.getProject().getProjectId();
    }
}
