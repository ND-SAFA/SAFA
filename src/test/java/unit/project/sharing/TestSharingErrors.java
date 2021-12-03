package unit.project.sharing;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.UUID;

import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectRole;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;

/**
 * Tests that useful error messages are provided for common scenarios including:
 * 1. User is not found
 * 2. User is already on the project
 */
public class TestSharingErrors extends BaseSharingTest {

    /**
     * Tests that error message notifies user that email is not registered
     * with an account when sharing to non-linked emails.
     *
     * @throws Exception Throws exception if http fails when sending get request.
     */
    @Test
    public void userNotFoundError() throws Exception {
        String projectName = "test-project";

        // Step - Create a project
        Project project = dbEntityBuilder
            .newProjectWithReturn(projectName);

        // Step - Share with non-existent user
        UUID projectId = project.getProjectId();
        String nonUserEmail = "non-existing@email.com";
        JSONObject response = shareProject(projectId, nonUserEmail, ProjectRole.VIEWER, status().is4xxClientError());

        // VP - Verify that error informs that email not associated with account
        String error = response.getJSONObject("body").getString("message");
        assertThat(error).matches(".*user.*exists.*email.*[\\s\\S]");
    }

    /**
     * Tests that user is notified that added email is already in the project.
     *
     * @throws Exception Throws exception if http fails when sending get request.
     */
    @Test
    public void userAlreadyInProjectError() throws Exception {
        String projectName = "test-project";

        // Step - Create a project
        Project project = createAndShareProject(projectName);

        // Step - Share project with same user again.
        JSONObject response = shareProject(
            project.getProjectId(),
            otherUserEmail,
            ProjectRole.VIEWER,
            status().is4xxClientError()
        );

        // VP - Verify that error message informs user that added email is already in the project
        String errorMessage = response.getJSONObject("body").getString("message");
        assertThat(errorMessage).matches(".*user.*project.*[\\s\\S]");
    }
}
