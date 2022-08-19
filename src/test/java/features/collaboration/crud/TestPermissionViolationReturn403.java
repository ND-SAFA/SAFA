package unit.project.sharing;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.builders.CommitBuilder;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;

/**
 * Responsible for verifying that violating a permission returns a 403 response.
 */
public class TestPermissionViolationReturn403 extends BaseSharingTest {
    String projectName = "project-name";

    @Test
    public void editViewOnlyProject() throws Exception {

        createAndShareProject(projectName);
        ProjectVersion projectVersion = this.dbEntityBuilder
            .newVersionWithReturn(projectName);

        // Step - Try
        System.out.println("Other:" + otherUser);
        loginUser(otherUser.getEmail(), otherUserPassword, true);
        CommitBuilder commitBuilder = CommitBuilder.withVersion(projectVersion).withAddedArtifact(new JSONObject());
        JSONObject response = commitWithStatus(commitBuilder, status().isForbidden());

        String message = response.getString("message");
        assertThat(message).contains("edit");
    }

    @Test
    public void other() throws Exception {
        createAndShareProject(projectName);
        loginUser(otherUser.getEmail(), otherUserPassword, true);
    }
}
