package edu.nd.crc.safa.test.features.memberships.permissions;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.Set;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.memberships.entities.db.OrganizationMembership;
import edu.nd.crc.safa.features.memberships.entities.db.ProjectMembership;
import edu.nd.crc.safa.features.memberships.entities.db.TeamMembership;
import edu.nd.crc.safa.features.organizations.entities.app.MembershipAppEntity;
import edu.nd.crc.safa.features.organizations.entities.db.Organization;
import edu.nd.crc.safa.features.organizations.entities.db.OrganizationRole;
import edu.nd.crc.safa.features.organizations.entities.db.ProjectRole;
import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.organizations.entities.db.TeamRole;
import edu.nd.crc.safa.features.permissions.entities.OrganizationPermission;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.features.permissions.entities.TeamPermission;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

public class TestMembershipPermissions extends AbstractPermissionViolationTest {

    private Organization organization;
    private Team team;

    @BeforeEach
    public void setup() {
        organization = serviceProvider.getOrganizationService().getOrganizationById(getCurrentUser().getDefaultOrgId());
        team = serviceProvider.getTeamService().getTeamById(organization.getFullOrgTeamId());
    }

    @Test
    public void testGetMembersWithProject() {
        test(
            () -> SafaRequest.withRoute(AppRoutes.Memberships.BY_ENTITY_ID)
                .withEntityId(project.getId())
                .getWithJsonObject(status().is4xxClientError()),
            Set.of(ProjectPermission.VIEW)
        );
    }

    @Test
    public void testGetMembersWithTeam() {
        test(
            () -> SafaRequest.withRoute(AppRoutes.Memberships.BY_ENTITY_ID)
                .withEntityId(team.getId())
                .getWithJsonObject(status().is4xxClientError()),
            Set.of(TeamPermission.VIEW)
        );
    }

    @Test
    public void testGetMembersWithOrg() {
        test(
            () -> SafaRequest.withRoute(AppRoutes.Memberships.BY_ENTITY_ID)
                .withEntityId(organization.getId())
                .getWithJsonObject(status().is4xxClientError()),
            Set.of(OrganizationPermission.VIEW)
        );
    }

    @Test
    public void testCreateProjectMembership() {
        MembershipAppEntity membership = new MembershipAppEntity();
        membership.setEmail(sharee.getEmail());
        membership.setRole("ADMIN");

        test(
            () -> SafaRequest.withRoute(AppRoutes.Memberships.Invites.BY_ENTITY_ID)
                .withEntityId(project.getId())
                .postWithJsonObject(membership, status().is4xxClientError()),
            Set.of(ProjectPermission.EDIT_MEMBERS)
        );
    }

    @Test
    public void testCreateTeamMembership() {
        MembershipAppEntity membership = new MembershipAppEntity();
        membership.setEmail(sharee.getEmail());
        membership.setRole("ADMIN");

        test(
            () -> SafaRequest.withRoute(AppRoutes.Memberships.Invites.BY_ENTITY_ID)
                .withEntityId(team.getId())
                .postWithJsonObject(membership, status().is4xxClientError()),
            Set.of(TeamPermission.EDIT_MEMBERS)
        );
    }

    @Test
    public void testCreateOrgMembership() {
        MembershipAppEntity membership = new MembershipAppEntity();
        membership.setEmail(sharee.getEmail());
        membership.setRole("ADMIN");

        test(
            () -> SafaRequest.withRoute(AppRoutes.Memberships.Invites.BY_ENTITY_ID)
                .withEntityId(organization.getId())
                .postWithJsonObject(membership, status().is4xxClientError()),
            Set.of(OrganizationPermission.EDIT_MEMBERS)
        );
    }

    @Test
    public void testModifyProjectMembership() {
        MembershipAppEntity membership = new MembershipAppEntity();
        membership.setEmail(currentUserName);
        membership.setRole("NONE");

        ProjectMembership projectMembership =
            (ProjectMembership) serviceProvider.getProjectMembershipService().getMembershipsForEntity(project).get(0);

        test(
            () -> SafaRequest.withRoute(AppRoutes.Memberships.BY_ENTITY_ID_AND_MEMBERSHIP_ID)
                .withEntityId(project.getId())
                .withMembershipId(projectMembership.getId())
                .putWithJsonObject(membership, status().is4xxClientError()),
            Set.of(ProjectPermission.EDIT_MEMBERS)
        );
    }

    @Test
    public void testModifyTeamMembership() {
        MembershipAppEntity membership = new MembershipAppEntity();
        membership.setEmail(currentUserName);
        membership.setRole("NONE");

        TeamMembership teamMembership =
            (TeamMembership) serviceProvider.getTeamMembershipService().getMembershipsForEntity(team).get(0);

        test(
            () -> SafaRequest.withRoute(AppRoutes.Memberships.BY_ENTITY_ID_AND_MEMBERSHIP_ID)
                .withEntityId(team.getId())
                .withMembershipId(teamMembership.getId())
                .putWithJsonObject(membership, status().is4xxClientError()),
            Set.of(TeamPermission.EDIT_MEMBERS)
        );
    }

    @Test
    public void testModifyOrganizationMembership() {
        MembershipAppEntity membership = new MembershipAppEntity();
        membership.setEmail(currentUserName);
        membership.setRole("NONE");

        OrganizationMembership orgMembership =
            (OrganizationMembership) serviceProvider.getOrgMembershipService().getMembershipsForEntity(organization).get(0);

        test(
            () -> SafaRequest.withRoute(AppRoutes.Memberships.BY_ENTITY_ID_AND_MEMBERSHIP_ID)
                .withEntityId(organization.getId())
                .withMembershipId(orgMembership.getId())
                .putWithJsonObject(membership, status().is4xxClientError()),
            Set.of(OrganizationPermission.EDIT_MEMBERS)
        );
    }

    @Test
    public void testDeleteProjectMembership() {
        SafaUser sharee = serviceProvider.getSafaUserService().getUserById(getSharee().getUserId());
        ProjectMembership shareeMembership =
            serviceProvider.getProjectMembershipService().addUserRole(sharee, project, ProjectRole.VIEWER);
        ProjectMembership ownerMembership =
            serviceProvider.getProjectMembershipService().addUserRole(getCurrentUser(), project, ProjectRole.OWNER);

        test(
            () -> SafaRequest.withRoute(AppRoutes.Memberships.BY_ENTITY_ID_AND_MEMBERSHIP_ID)
                .withEntityId(project.getId())
                .withMembershipId(ownerMembership.getId())
                .deleteWithJsonObject(status().is4xxClientError()),
            Set.of(ProjectPermission.EDIT_MEMBERS)
        );

        SafaRequest.withRoute(AppRoutes.Memberships.BY_ENTITY_ID_AND_MEMBERSHIP_ID)
            .withEntityId(project.getId())
            .withMembershipId(shareeMembership.getId())
            .deleteWithJsonObject(status().is2xxSuccessful());
    }

    @Test
    public void testDeleteTeamMembership() {
        SafaUser sharee = serviceProvider.getSafaUserService().getUserById(getSharee().getUserId());
        TeamMembership shareeMembership =
            serviceProvider.getTeamMembershipService().addUserRole(sharee, team, TeamRole.VIEWER);
        TeamMembership ownerMembership =
            serviceProvider.getTeamMembershipService().addUserRole(getCurrentUser(), team, TeamRole.ADMIN);

        test(
            () -> SafaRequest.withRoute(AppRoutes.Memberships.BY_ENTITY_ID_AND_MEMBERSHIP_ID)
                .withEntityId(team.getId())
                .withMembershipId(ownerMembership.getId())
                .deleteWithJsonObject(status().is4xxClientError()),
            Set.of(TeamPermission.EDIT_MEMBERS)
        );

        SafaRequest.withRoute(AppRoutes.Memberships.BY_ENTITY_ID_AND_MEMBERSHIP_ID)
            .withEntityId(team.getId())
            .withMembershipId(shareeMembership.getId())
            .deleteWithJsonObject(status().is2xxSuccessful());
    }

    @Test
    public void testDeleteOrgMembership() {
        SafaUser sharee = serviceProvider.getSafaUserService().getUserById(getSharee().getUserId());
        OrganizationMembership shareeMembership =
            serviceProvider.getOrgMembershipService().addUserRole(sharee, organization, OrganizationRole.MEMBER);
        OrganizationMembership ownerMembership =
            serviceProvider.getOrgMembershipService().addUserRole(getCurrentUser(), organization, OrganizationRole.ADMIN);

        test(
            () -> SafaRequest.withRoute(AppRoutes.Memberships.BY_ENTITY_ID_AND_MEMBERSHIP_ID)
                .withEntityId(organization.getId())
                .withMembershipId(ownerMembership.getId())
                .deleteWithJsonObject(status().is4xxClientError()),
            Set.of(OrganizationPermission.EDIT_MEMBERS)
        );

        SafaRequest.withRoute(AppRoutes.Memberships.BY_ENTITY_ID_AND_MEMBERSHIP_ID)
            .withEntityId(organization.getId())
            .withMembershipId(shareeMembership.getId())
            .deleteWithJsonObject(status().is2xxSuccessful());
    }

    @Test
    public void testRemoveUserFromProject() {
        test(
            () -> SafaRequest.withRoute(AppRoutes.Memberships.BY_ENTITY_ID)
                .withEntityId(project.getId())
                .withQueryParam("userEmail", currentUserName)
                .deleteWithJsonObject(status().is4xxClientError()),
            Set.of(ProjectPermission.EDIT_MEMBERS)
        );
    }

    @Test
    public void testRemoveUserFromTeam() {
        test(
            () -> SafaRequest.withRoute(AppRoutes.Memberships.BY_ENTITY_ID)
                .withEntityId(team.getId())
                .withQueryParam("userEmail", currentUserName)
                .deleteWithJsonObject(status().is4xxClientError()),
            Set.of(TeamPermission.EDIT_MEMBERS)
        );
    }

    @Test
    public void testRemoveUserFromOrganization() {
        test(
            () -> SafaRequest.withRoute(AppRoutes.Memberships.BY_ENTITY_ID)
                .withEntityId(organization.getId())
                .withQueryParam("userEmail", currentUserName)
                .deleteWithJsonObject(status().is4xxClientError()),
            Set.of(OrganizationPermission.EDIT_MEMBERS)
        );
    }

    @Override
    protected ProjectRole getShareePermission() {
        return ProjectRole.NONE;
    }

}
