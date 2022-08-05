package unit.project.sharing;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import edu.nd.crc.safa.builders.requests.SafaRequest;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.projects.entities.db.Project;

import org.json.JSONArray;
import org.junit.jupiter.api.Test;

/**
 * Tests that projects defined in database are able to be retrieved by user.
 */
class TestProjectRetrievalWithSharing extends BaseSharingTest {

    /**
     * Tests that a user is able to retrieve all the projects they own.
     *
     * @throws Exception Throws exception if http fails when sending get request.
     */
    @Test
    void sharedProjectAppearsInGetProjects() throws Exception {
        String projectName = "test-project";

        // Step - Create and share a project.
        createAndShareProject(projectName);

        // Step - Get projects for user who got shared with
        JSONArray projects = SafaRequest.withRoute(AppRoutes.Projects.GET_PROJECTS).getWithJsonArray();

        // VP - Verify that shared project is visible
        assertThat(projects.length()).isEqualTo(1);
        assertThat(projects.getJSONObject(0).getString("name")).isEqualTo(projectName);
    }

    @Test
    void retrieveProjectMembers() throws Exception {
        String projectName = "test-project";

        // Step - Create and share a project.
        Project project = createAndShareProject(projectName);

        // Step - Get projects for user who got shared with
        JSONArray members = getProjectMembers(project);

        // VP - Verify that shared project is visible
        assertThat(members.length()).isEqualTo(2);
        String otherUserEmail = "doesNotExist@gmail.com";
        assertThat(members.getJSONObject(1).getString("email")).isEqualTo(otherUserEmail);
    }
}
