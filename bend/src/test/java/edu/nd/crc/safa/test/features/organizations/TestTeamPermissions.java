package edu.nd.crc.safa.test.features.organizations;

import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.Set;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.organizations.entities.app.TeamAppEntity;
import edu.nd.crc.safa.features.organizations.entities.db.Team;
import edu.nd.crc.safa.features.permissions.entities.OrganizationPermission;
import edu.nd.crc.safa.features.permissions.entities.TeamPermission;
import edu.nd.crc.safa.test.features.memberships.permissions.AbstractPermissionViolationTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

public class TestTeamPermissions extends AbstractPermissionViolationTest {

    private Team team;

    @BeforeEach
    public void getTeam() {
        team = serviceProvider.getTeamService().getPersonalTeam(getCurrentUser());
    }

    @Test
    public void testGetTeam() {
        test(
            () -> SafaRequest.withRoute(AppRoutes.Organizations.Teams.BY_ID)
                .withTeamId(team.getId())
                .withOrgId(team.getOrganization().getId())
                .getWithJsonObject(status().is4xxClientError()),
            Set.of(TeamPermission.VIEW, OrganizationPermission.VIEW_TEAMS)
        );
    }

    @Test
    public void testGetOrgTeam() {
        test(
            () -> SafaRequest.withRoute(AppRoutes.Organizations.Teams.SELF)
                .withOrgId(team.getOrganization().getId())
                .getWithJsonObject(status().is4xxClientError()),
            Set.of(TeamPermission.VIEW, OrganizationPermission.VIEW_TEAMS)
        );
    }

    @Test
    public void testCreateTeam() {
        TeamAppEntity teamDefinition = new TeamAppEntity();
        test(
            () -> SafaRequest.withRoute(AppRoutes.Organizations.Teams.ROOT)
                .withOrgId(team.getOrganization().getId())
                .postWithJsonObject(teamDefinition, status().is4xxClientError()),
            Set.of(OrganizationPermission.CREATE_TEAMS)
        );
    }

    @Test
    public void testUpdateTeam() {
        TeamAppEntity teamDefinition = new TeamAppEntity();
        test(
            () -> SafaRequest.withRoute(AppRoutes.Organizations.Teams.BY_ID)
                .withOrgId(team.getOrganization().getId())
                .withTeamId(team.getId())
                .putWithJsonObject(teamDefinition, status().is4xxClientError()),
            Set.of(TeamPermission.EDIT)
        );
    }

    @Test
    public void testDeleteTeam() {
        test(
            () -> SafaRequest.withRoute(AppRoutes.Organizations.Teams.BY_ID)
                .withOrgId(team.getOrganization().getId())
                .withTeamId(team.getId())
                .deleteWithJsonObject(status().is4xxClientError()),
            Set.of(TeamPermission.DELETE, OrganizationPermission.DELETE_TEAMS)
        );
    }
}
