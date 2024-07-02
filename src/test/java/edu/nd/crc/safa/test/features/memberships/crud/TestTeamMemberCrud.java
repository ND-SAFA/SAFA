package edu.nd.crc.safa.test.features.memberships.crud;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.List;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.organizations.entities.app.MembershipAppEntity;
import edu.nd.crc.safa.features.organizations.entities.app.MembershipType;
import edu.nd.crc.safa.features.organizations.entities.app.OrganizationAppEntity;
import edu.nd.crc.safa.features.organizations.entities.app.TeamAppEntity;
import edu.nd.crc.safa.features.organizations.entities.db.TeamRole;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.SafaRequest;
import edu.nd.crc.safa.test.services.UserUtils;

import com.fasterxml.jackson.core.type.TypeReference;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

public class TestTeamMemberCrud extends ApplicationBaseTest {

    private static final String otherEmail = "email@email.com";
    private static final String otherPassword = "password";
    private static final String otherRole = TeamRole.VIEWER.name();
    private static final String secondRole = TeamRole.EDITOR.name();
    private TeamAppEntity team;
    private MembershipAppEntity newMembership;

    @BeforeEach
    public void createOtherUser() throws Exception {
        this.authorizationService.createUser(otherEmail, otherPassword);
        OrganizationAppEntity org = SafaRequest.withRoute(AppRoutes.Organizations.SELF)
            .getAsType(new TypeReference<>(){});
        team = org.getTeams().get(0);
    }

    @Test
    public void testTeamMemberCrud() throws Exception {
        testCreateMembership();
        testRetrieveMembership();
        testUpdateMembership();
        testDeleteMembership();
        testDeleteAllMemberships();
    }

    private void testCreateMembership() throws Exception {
        MembershipAppEntity membershipDefinition = new MembershipAppEntity(otherEmail, otherRole);

        newMembership =
            UserUtils.asActiveSuperuser(getCurrentUser(),
                () -> SafaRequest.withRoute(AppRoutes.Memberships.BY_ENTITY_ID)
                    .withEntityId(team.getId())
                    .postAndParseResponse(membershipDefinition, new TypeReference<>(){}));

        assertMembership(newMembership, otherRole);
    }

    private void testRetrieveMembership() throws Exception {
        List<MembershipAppEntity> memberships =
            SafaRequest.withRoute(AppRoutes.Memberships.BY_ENTITY_ID)
                .withEntityId(team.getId())
                .getAsType(new TypeReference<>(){});

        assertThat(memberships.size()).isEqualTo(2);

        boolean equalFound = false;
        for (MembershipAppEntity membership : memberships) {
            if (membership.equals(newMembership)) {
                equalFound = true;
                break;
            }
        }
        assertThat(equalFound).isTrue();
    }

    private void testUpdateMembership() throws Exception {
        MembershipAppEntity updatedMembershipDefinition = new MembershipAppEntity(otherEmail, secondRole);

        newMembership =
            SafaRequest.withRoute(AppRoutes.Memberships.BY_ENTITY_ID_AND_MEMBERSHIP_ID)
                .withEntityId(team.getId())
                .withMembershipId(newMembership.getId())
                .putAndParseResponse(updatedMembershipDefinition, new TypeReference<>(){});

        assertMembership(newMembership, secondRole);
    }

    private void assertMembership(MembershipAppEntity membership, String role) {
        assertThat(membership).isNotNull();
        assertThat(membership.getEmail()).isEqualTo(otherEmail);
        assertThat(membership.getRole()).isEqualTo(role);
        assertThat(membership.getId()).isNotNull();
        assertThat(membership.getEntityId()).isEqualTo(team.getId());
        assertThat(membership.getEntityType()).isEqualTo(MembershipType.TEAM);
    }

    private void testDeleteMembership() throws Exception {
        SafaRequest.withRoute(AppRoutes.Memberships.BY_ENTITY_ID_AND_MEMBERSHIP_ID)
            .withEntityId(team.getId())
            .withMembershipId(newMembership.getId())
            .deleteWithJsonObject();

        List<MembershipAppEntity> memberships =
            SafaRequest.withRoute(AppRoutes.Memberships.BY_ENTITY_ID)
                .withEntityId(team.getId())
                .getAsType(new TypeReference<>(){});

        assertThat(memberships.size()).isEqualTo(1);
        assertThat(memberships.get(0).getEmail()).isNotEqualTo(otherEmail);
    }

    private void testDeleteAllMemberships() throws Exception {
        createTwoMemberships();

        SafaRequest.withRoute(AppRoutes.Memberships.BY_ENTITY_ID)
            .withEntityId(team.getId())
            .withQueryParam("userEmail", otherEmail)
            .deleteWithJsonObject();

        List<MembershipAppEntity> memberships =
            SafaRequest.withRoute(AppRoutes.Memberships.BY_ENTITY_ID)
                .withEntityId(team.getId())
                .getAsType(new TypeReference<>(){});
        assertThat(memberships.size()).isEqualTo(1);
        assertThat(memberships.get(0).getEmail()).isNotEqualTo(otherEmail);
    }

    private void createTwoMemberships() throws Exception {
        MembershipAppEntity membershipDefinition1 = new MembershipAppEntity(otherEmail, otherRole);
        UserUtils.asActiveSuperuser(getCurrentUser(), () -> SafaRequest.withRoute(AppRoutes.Memberships.BY_ENTITY_ID)
            .withEntityId(team.getId())
            .postAndParseResponse(membershipDefinition1, new TypeReference<>(){}));

        MembershipAppEntity membershipDefinition2 = new MembershipAppEntity(otherEmail, secondRole);
        UserUtils.asActiveSuperuser(getCurrentUser(), () -> SafaRequest.withRoute(AppRoutes.Memberships.BY_ENTITY_ID)
            .withEntityId(team.getId())
            .postAndParseResponse(membershipDefinition2, new TypeReference<>(){}));

        List<MembershipAppEntity> memberships =
            SafaRequest.withRoute(AppRoutes.Memberships.BY_ENTITY_ID)
                .withEntityId(team.getId())
                .getAsType(new TypeReference<>(){});
        assertThat(memberships.size()).isEqualTo(3);
    }
}
