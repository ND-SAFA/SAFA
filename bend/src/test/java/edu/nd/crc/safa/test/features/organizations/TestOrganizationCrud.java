package edu.nd.crc.safa.test.features.organizations;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.List;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.organizations.entities.app.MembershipAppEntity;
import edu.nd.crc.safa.features.organizations.entities.app.MembershipType;
import edu.nd.crc.safa.features.organizations.entities.app.OrganizationAppEntity;
import edu.nd.crc.safa.features.organizations.entities.app.TeamAppEntity;
import edu.nd.crc.safa.features.organizations.entities.db.OrganizationRole;
import edu.nd.crc.safa.features.organizations.entities.db.TeamRole;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import com.fasterxml.jackson.core.type.TypeReference;
import com.google.common.base.Functions;
import org.junit.jupiter.api.Test;

public class TestOrganizationCrud extends ApplicationBaseTest {

    private static final OrganizationAppEntity orgDefinition = new OrganizationAppEntity(
        "Test Organization",
        "Test Organization Description"
    );

    private static final OrganizationAppEntity updatedOrgDefinition = new OrganizationAppEntity(
        "New Name",
        "New Description"
    );

    private OrganizationAppEntity createdOrg;

    @Test
    public void testOrganizationCrud() throws Exception {
        rootBuilder.getCommonRequestService().user()
            .makeUserSuperuser(getCurrentUser())
            .activateSuperuser();

        testDefaultOrganization();
        testCreateOrganization();
        testRetrieveOrganization();
        testUpdateOrganization();
        testDeleteOrganization();
    }

    private void testDefaultOrganization() throws Exception {
        List<OrganizationAppEntity> userOrgs =
            SafaRequest.withRoute(AppRoutes.Organizations.ROOT)
                .getAsType(new TypeReference<>() {
                });

        assertEquals(1, userOrgs.size());
        OrganizationAppEntity org = userOrgs.get(0);
        assertOrg(org, getCurrentUser().getEmail(), "");
        assertTrue(org.isPersonalOrg());

        OrganizationAppEntity personalOrg =
            SafaRequest.withRoute(AppRoutes.Organizations.SELF)
                .getAsType(new TypeReference<>() {
                });
        assertEquals(org, personalOrg);
    }

    private void assertOrg(OrganizationAppEntity org, String orgName, String orgDescription) {
        assertEquals(orgName, org.getName());
        assertEquals(orgDescription, org.getDescription());

        List<MembershipAppEntity> memberships = org.getMembers();
        assertEquals(1, memberships.size());
        MembershipAppEntity membership = memberships.get(0);
        assertEquals(getCurrentUser().getEmail(), membership.getEmail());
        assertEquals(MembershipType.ORGANIZATION, membership.getEntityType());
        assertEquals(OrganizationRole.ADMIN.name(), membership.getRole());
        assertEquals(org.getId(), membership.getEntityId());

        List<TeamAppEntity> teams = org.getTeams();
        assertEquals(1, teams.size());
        TeamAppEntity team = teams.get(0);
        assertEquals(orgName, team.getName());

        List<MembershipAppEntity> teamMemberships = team.getMembers();
        assertEquals(1, teamMemberships.size());
        MembershipAppEntity teamMembership = teamMemberships.get(0);
        assertEquals(getCurrentUser().getEmail(), teamMembership.getEmail());
        assertEquals(MembershipType.TEAM, teamMembership.getEntityType());
        assertEquals(TeamRole.ADMIN.name(), teamMembership.getRole());
        assertEquals(team.getId(), teamMembership.getEntityId());
    }

    private void testCreateOrganization() throws Exception {
        createdOrg =
            SafaRequest.withRoute(AppRoutes.Organizations.ROOT)
                .postAndParseResponse(orgDefinition, new TypeReference<>() {
                });

        assertNotNull(createdOrg.getId());
        assertOrg(createdOrg, orgDefinition.getName(), orgDefinition.getDescription());
        assertFalse(createdOrg.isPersonalOrg());
    }

    private void testRetrieveOrganization() throws Exception {
        OrganizationAppEntity org =
            SafaRequest.withRoute(AppRoutes.Organizations.BY_ID)
                .withOrgId(createdOrg.getId())
                .getAsType(new TypeReference<>() {
                });

        assertEquals(createdOrg, org);
    }

    private void testUpdateOrganization() throws Exception {
        OrganizationAppEntity updatedOrg =
            SafaRequest.withRoute(AppRoutes.Organizations.BY_ID)
                .withOrgId(createdOrg.getId())
                .putAndParseResponse(updatedOrgDefinition, new TypeReference<>() {
                });

        assertEquals(updatedOrgDefinition.getName(), updatedOrg.getName());
        assertEquals(updatedOrgDefinition.getDescription(), updatedOrg.getDescription());
    }

    private void testDeleteOrganization() throws Exception {
        SafaRequest.withRoute(AppRoutes.Organizations.BY_ID)
            .withOrgId(createdOrg.getId())
            .deleteWithJsonObject();

        String result =
            SafaRequest.withRoute(AppRoutes.Organizations.BY_ID)
                .withOrgId(createdOrg.getId())
                .getWithResponseParser(Functions.identity(), status().isNotFound());
        assertTrue(result.contains("No organization with the given ID found"));
    }
}
