package edu.nd.crc.safa.test.features.organizations;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.organizations.entities.app.MembershipAppEntity;
import edu.nd.crc.safa.features.organizations.entities.app.MembershipType;
import edu.nd.crc.safa.features.organizations.entities.app.OrganizationAppEntity;
import edu.nd.crc.safa.features.organizations.entities.app.TeamAppEntity;
import edu.nd.crc.safa.features.organizations.entities.db.TeamRole;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import com.fasterxml.jackson.core.type.TypeReference;
import com.google.common.base.Functions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

public class TestTeamCrud extends ApplicationBaseTest {

    private static final TeamAppEntity teamDefinition = new TeamAppEntity("Test Team");
    private static final TeamAppEntity updatedTeamDefinition = new TeamAppEntity("Updated Team");

    private UUID defaultOrgId;
    private TeamAppEntity createdTeam;

    @BeforeEach
    public void setup() throws Exception {
        OrganizationAppEntity defaultOrg =
            SafaRequest.withRoute(AppRoutes.Organizations.SELF)
                .getAsType(new TypeReference<>() {
                });

        assertNotNull(defaultOrg);
        assertNotNull(defaultOrg.getId());
        defaultOrgId = defaultOrg.getId();
    }

    @Test
    public void testTeamCrud() throws Exception {
        testDefaultTeam();
        testCreateTeam();
        testRetrieveTeam();
        testUpdateTeam();
        testDeleteTeam();
    }

    private void testDefaultTeam() throws Exception {
        List<TeamAppEntity> defaultOrgTeams =
            SafaRequest.withRoute(AppRoutes.Organizations.Teams.ROOT)
                .withOrgId(defaultOrgId)
                .getAsType(new TypeReference<>() {
                });

        assertEquals(1, defaultOrgTeams.size());
        TeamAppEntity defaultOrgTeam = defaultOrgTeams.get(0);
        assertEquals(getCurrentUser().getEmail(), defaultOrgTeam.getName());

        List<MembershipAppEntity> teamMemberships = defaultOrgTeam.getMembers();
        assertEquals(1, teamMemberships.size());
        MembershipAppEntity teamMembership = teamMemberships.get(0);
        assertEquals(getCurrentUser().getEmail(), teamMembership.getEmail());
        assertEquals(MembershipType.TEAM, teamMembership.getEntityType());
        assertEquals(TeamRole.ADMIN.name(), teamMembership.getRole());
        assertEquals(defaultOrgTeam.getId(), teamMembership.getEntityId());

        TeamAppEntity defaultTeam =
            SafaRequest.withRoute(AppRoutes.Organizations.Teams.SELF)
                .withOrgId(defaultOrgId)
                .getAsType(new TypeReference<>() {
                });

        assertEquals(defaultOrgTeam, defaultTeam);
    }

    private void testCreateTeam() throws Exception {
        createdTeam = SafaRequest.withRoute(AppRoutes.Organizations.Teams.ROOT)
            .withOrgId(defaultOrgId)
            .postAndParseResponse(teamDefinition, new TypeReference<>() {
            });

        assertEquals(teamDefinition.getName(), createdTeam.getName());

        List<MembershipAppEntity> teamMemberships = createdTeam.getMembers();
        assertEquals(1, teamMemberships.size());
        MembershipAppEntity teamMembership = teamMemberships.get(0);
        assertEquals(getCurrentUser().getEmail(), teamMembership.getEmail());
        assertEquals(MembershipType.TEAM, teamMembership.getEntityType());
        assertEquals(TeamRole.ADMIN.name(), teamMembership.getRole());
        assertEquals(createdTeam.getId(), teamMembership.getEntityId());
    }

    private void testRetrieveTeam() throws Exception {
        TeamAppEntity retrievedTeam =
            SafaRequest.withRoute(AppRoutes.Organizations.Teams.BY_ID)
                .withOrgId(defaultOrgId)
                .withTeamId(createdTeam.getId())
                .getAsType(new TypeReference<>() {
                });

        assertEquals(createdTeam, retrievedTeam);
    }

    private void testUpdateTeam() throws Exception {
        TeamAppEntity updatedTeam =
            SafaRequest.withRoute(AppRoutes.Organizations.Teams.BY_ID)
                .withOrgId(defaultOrgId)
                .withTeamId(createdTeam.getId())
                .putAndParseResponse(updatedTeamDefinition, new TypeReference<>() {
                });

        assertEquals(updatedTeamDefinition.getName(), updatedTeam.getName());
    }

    private void testDeleteTeam() throws Exception {
        SafaRequest.withRoute(AppRoutes.Organizations.Teams.BY_ID)
            .withOrgId(defaultOrgId)
            .withTeamId(createdTeam.getId())
            .deleteWithJsonObject();

        String result =
            SafaRequest.withRoute(AppRoutes.Organizations.Teams.BY_ID)
                .withOrgId(defaultOrgId)
                .withTeamId(createdTeam.getId())
                .getWithResponseParser(Functions.identity(), status().isNotFound());

        assertThat(result).contains("No team with the given ID found");
    }
}
