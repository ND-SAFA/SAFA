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

        // VP - Verify no users on project
        assertThat(members.length()).isEqualTo(0);
    }

    @Test
    void testRemoveSelfWithoutEditPermission() throws Exception {
        authorizationService.loginUser(Sharee.email, Sharee.password, this);
        authorizationService.removeMemberFromProject(project, Sharee.email);
    }
}
