package unit.project.sharing;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectRole;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;

/**
 * Tests that projects defined in database are able to be retrieved by user.
 */
public class UpdateAndDeleteMemberships extends BaseSharingTest {

    /**
     * Tests that a project role can be modified.
     *
     * @throws Exception Throws exception if http fails when sending get request.
     */
    @Test
    public void updateProjectMembership() throws Exception {
        String projectName = "test-project";

        // Step - Create and share a project.
        Project project = createAndShareProject(projectName);

        // Step - Update project member with new role
        shareProject(project, otherUserEmail, ProjectRole.ADMIN, status().is2xxSuccessful());

        // Step - Get project members
        JSONArray response = getProjectMembers(project);

        // VP - Verify that new role is reflected
        JSONObject membership = getMembershipWithEmail(response, otherUserEmail);
        assertThat(membership.getString("role")).isEqualTo(ProjectRole.ADMIN.toString());
    }

    /**
     * Tests that project memberships can be deleted.
     *
     * @throws SafaError If http fails.
     */
    @Test
    public void testDeleteMembership() throws Exception {

        String projectName = "test-project";

        // Step - Create and share a project.
        Project project = createAndShareProject(projectName);

        // Step - Delete project member
        removeMemberFromProject(project, this.otherUser.getEmail());

        // Step - Get members
        JSONArray members = getProjectMembers(project);

        // VP - Verify that member is not in list
        assertThat(members.length()).isEqualTo(1);
        assertThat(members.getJSONObject(0).getString("email")).isEqualTo(currentUser.getEmail());
    }

    private JSONObject getMembershipWithEmail(JSONArray memberships, String email) throws SafaError {
        for (int i = 0; i < memberships.length(); i++) {
            JSONObject membership = memberships.getJSONObject(i);
            if (membership.getString("email").equals(email)) {
                return membership;
            }
        }
        throw new SafaError("Could not find membership with email:" + email);
    }
}
