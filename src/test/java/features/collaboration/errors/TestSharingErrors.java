package features.collaboration.errors;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.ProjectRole;

import features.collaboration.base.AbstractCollaborationTest;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;

/**
 * Tests that useful error messages are provided for common scenarios including:
 * 1. User is not found
 * 2. User is already on the project
 */
class TestSharingErrors extends AbstractCollaborationTest {

    /**
     * Tests that error message notifies user that email is not registered
     * with an account when sharing to non-linked emails.
     *
     * @throws Exception Throws exception if http fails when sending get request.
     */
    @Test
    void userNotFoundError() throws Exception {
        String projectName = "test-project";

        // Step - Create a project
        Project project = dbEntityBuilder
            .newProjectWithReturn(projectName);

        // Step - Share with non-existent user
        String nonUserEmail = "non-existing@email.com";
        JSONObject response = setupTestService.shareProject(project, nonUserEmail, ProjectRole.VIEWER,
            status().is4xxClientError());

        // VP - Verify that error informs that email not associated with account
        String error = response.getString("message");
        assertThat(error).matches(".*user.*exists.*email.*[\\s\\S]");
    }
}
