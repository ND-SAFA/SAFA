package unit.project.sharing;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.Optional;

import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectMembership;
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
        JSONObject response = getProjectMembers(project);

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
        Optional<ProjectMembership> query = this.projectMembershipRepository.findByProjectAndMember(project,
            this.otherUser);
        String url = RouteBuilder
            .withRoute(AppRoutes.Projects.deleteProjectMembership)
            .withProjectMembership(query.get())
            .get();
        sendDelete(url, status().isNoContent());

        // Step - Get members
        JSONObject response = getProjectMembers(project);

        // VP - Verify that member is not in list
        JSONArray members = response.getJSONArray("body");
        assertThat(members.length()).isEqualTo(1);
        assertThat(members.getJSONObject(0).getString("email")).isEqualTo(currentUser.getEmail());
    }

    private JSONObject getMembershipWithEmail(JSONObject response, String email) throws SafaError {
        JSONArray memberships = response.getJSONArray("body");
        for (int i = 0; i < memberships.length(); i++) {
            JSONObject membership = memberships.getJSONObject(i);
            if (membership.getString("email").equals(email)) {
                return membership;
            }
        }
        throw new SafaError("Could not find membership with email:" + email);
    }
}
