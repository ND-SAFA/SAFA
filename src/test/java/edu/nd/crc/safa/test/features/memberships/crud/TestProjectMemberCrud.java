package edu.nd.crc.safa.test.features.memberships.crud;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.List;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.organizations.entities.app.MembershipAppEntity;
import edu.nd.crc.safa.features.organizations.entities.app.MembershipType;
import edu.nd.crc.safa.features.organizations.entities.db.ProjectRole;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import com.fasterxml.jackson.core.type.TypeReference;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

public class TestProjectMemberCrud extends ApplicationBaseTest {

    private static final String otherEmail = "email@email.com";
    private static final String otherPassword = "password";
    private static final String otherRole = ProjectRole.VIEWER.name();
    private static final String secondRole = ProjectRole.EDITOR.name();
    private Project project;
    private MembershipAppEntity newMembership;

    @BeforeEach
    public void createOtherUser() throws Exception {
        this.authorizationService.createUser(otherEmail, otherPassword);
        project = dbEntityBuilder.newProjectWithReturn(projectName);
    }

    @Test
    public void testProjectMemberCrud() throws Exception {
        testCreateMembership();
        testRetrieveMembership();
        testUpdateMembership();
        testDeleteMembership();
        testDeleteAllMemberships();
    }

    private void testCreateMembership() throws Exception {
        MembershipAppEntity membershipDefinition = new MembershipAppEntity(otherEmail, otherRole);

        newMembership =
            SafaRequest.withRoute(AppRoutes.Memberships.BY_ENTITY_ID)
                .withEntityId(project.getProjectId())
                .postAndParseResponse(membershipDefinition, new TypeReference<>(){});

        assertMembership(newMembership, otherRole);
    }

    private void testRetrieveMembership() throws Exception {
        List<MembershipAppEntity> memberships =
            SafaRequest.withRoute(AppRoutes.Memberships.BY_ENTITY_ID)
                .withEntityId(project.getProjectId())
                .getAsType(new TypeReference<>(){});

        assertThat(memberships.size()).isEqualTo(1);
        assertThat(memberships.get(0)).isEqualTo(newMembership);
    }

    private void testUpdateMembership() throws Exception {
        MembershipAppEntity updatedMembershipDefinition = new MembershipAppEntity(otherEmail, secondRole);

        newMembership =
            SafaRequest.withRoute(AppRoutes.Memberships.BY_ENTITY_ID_AND_MEMBERSHIP_ID)
                .withEntityId(project.getProjectId())
                .withMembershipId(newMembership.getId())
                .putAndParseResponse(updatedMembershipDefinition, new TypeReference<>(){});

        assertMembership(newMembership, secondRole);
    }

    private void assertMembership(MembershipAppEntity membership, String role) {
        assertThat(membership).isNotNull();
        assertThat(membership.getEmail()).isEqualTo(otherEmail);
        assertThat(membership.getRole()).isEqualTo(role);
        assertThat(membership.getId()).isNotNull();
        assertThat(membership.getEntityId()).isEqualTo(project.getProjectId());
        assertThat(membership.getEntityType()).isEqualTo(MembershipType.PROJECT);
    }

    private void testDeleteMembership() throws Exception {
        SafaRequest.withRoute(AppRoutes.Memberships.BY_ENTITY_ID_AND_MEMBERSHIP_ID)
            .withEntityId(project.getProjectId())
            .withMembershipId(newMembership.getId())
            .deleteWithJsonObject();

        List<MembershipAppEntity> memberships =
            SafaRequest.withRoute(AppRoutes.Memberships.BY_ENTITY_ID)
                .withEntityId(project.getProjectId())
                .getAsType(new TypeReference<>(){});

        assertThat(memberships.size()).isEqualTo(0);
    }

    private void testDeleteAllMemberships() throws Exception {
        createTwoMemberships();

        SafaRequest.withRoute(AppRoutes.Memberships.BY_ENTITY_ID)
            .withEntityId(project.getProjectId())
            .withQueryParam("userEmail", otherEmail)
            .deleteWithJsonObject();

        List<MembershipAppEntity> memberships =
            SafaRequest.withRoute(AppRoutes.Memberships.BY_ENTITY_ID)
                .withEntityId(project.getProjectId())
                .getAsType(new TypeReference<>(){});
        assertThat(memberships.size()).isEqualTo(0);
    }

    private void createTwoMemberships() throws Exception {
        MembershipAppEntity membershipDefinition = new MembershipAppEntity(otherEmail, otherRole);
        SafaRequest.withRoute(AppRoutes.Memberships.BY_ENTITY_ID)
            .withEntityId(project.getProjectId())
            .postAndParseResponse(membershipDefinition, new TypeReference<>(){});

        membershipDefinition = new MembershipAppEntity(otherEmail, secondRole);
        SafaRequest.withRoute(AppRoutes.Memberships.BY_ENTITY_ID)
            .withEntityId(project.getProjectId())
            .postAndParseResponse(membershipDefinition, new TypeReference<>(){});

        List<MembershipAppEntity> memberships =
            SafaRequest.withRoute(AppRoutes.Memberships.BY_ENTITY_ID)
                .withEntityId(project.getProjectId())
                .getAsType(new TypeReference<>(){});
        assertThat(memberships.size()).isEqualTo(2);
    }
}
