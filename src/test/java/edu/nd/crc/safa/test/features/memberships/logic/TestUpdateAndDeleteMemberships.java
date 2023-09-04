package edu.nd.crc.safa.test.features.memberships.logic;

import static org.assertj.core.api.Assertions.assertThat;

import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.test.common.AbstractSharingTest;

import org.json.JSONArray;
import org.junit.jupiter.api.Test;

/**
 * Tests that projects defined in database are to be retrieved by user.
 */
class TestUpdateAndDeleteMemberships extends AbstractSharingTest {

    /**
     * Tests that project memberships can be deleted.
     *
     * @throws SafaError If http fails.
     */
    @Test
    void testDeleteMembership() throws Exception {
        // Step - Delete project member
        authorizationService.removeMemberFromProject(
            project,
            Sharee.email);

        // Step - Get members
        JSONArray members = retrievalService.getProjectMembers(project);

        // VP - Verify that single member on project
        assertThat(members.length()).isEqualTo(1);

        // VP - Verify that member email is correct
        String memberEmail = members.getJSONObject(0).getString("email");
        assertThat(memberEmail).isEqualTo(currentUser.getEmail());
    }

    @Test
    void testRemoveSelfWithoutEditPermission() throws Exception {
        authorizationService.loginUser(Sharee.email, Sharee.password);
        authorizationService.removeMemberFromProject(project, Sharee.email);
    }
}
