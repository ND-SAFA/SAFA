package unit.project.sharing;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.db.Project;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;

/**
 * Tests that projects defined in database are able to be retrieved by user.
 */
public class TestProjectRetrievalWithSharing extends BaseSharingTest {

    private final String otherUserEmail = "doesNotExist@gmail.com";
    private final String otherUserPassword = "somePassword";

    /**
     * Tests that a user is able to retrieve all the projects they own.
     *
     * @throws Exception Throws exception if http fails when sending get request.
     */
    @Test
    public void sharedProjectAppearsInGetProjects() throws Exception {
        String projectName = "test-project";

        // Step - Create and share a project.
        createAndShareProject(projectName);

        // Step - Get projects for user who got shared with
        JSONObject response = sendGet(AppRoutes.Projects.projects, status().is2xxSuccessful());

        // VP - Verify that shared project is visible
        assertThat(response.getJSONArray("body").length()).isEqualTo(1);
        JSONArray projects = response.getJSONArray("body");
        assertThat(projects.getJSONObject(0).getString("name")).isEqualTo(projectName);
    }

    @Test
    public void retrieveProjectMembers() throws Exception {
        String projectName = "test-project";

        // Step - Create and share a project.
        Project project = createAndShareProject(projectName);

        // Step - Get projects for user who got shared with
        String url = RouteBuilder
            .withRoute(AppRoutes.Projects.getProjectMembers)
            .withProject(project)
            .get();
        JSONObject response = sendGet(url, status().is2xxSuccessful());

        // VP - Verify that shared project is visible
        assertThat(response.getJSONArray("body").length()).isEqualTo(2);
        JSONArray members = response.getJSONArray("body");
        assertThat(members.getJSONObject(1).getString("email")).isEqualTo(otherUserEmail);
    }
}
