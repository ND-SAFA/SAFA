package features.utilities;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.UUID;

import edu.nd.crc.safa.builders.requests.SafaRequest;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.projects.entities.db.Project;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import features.base.ApplicationBaseTest;

/**
 * Tests that server errors include a
 * - status (0 if success otherwise some error code > 0)
 * - body (contains error message and other information)
 */
class TestSafaErrorMessage extends ApplicationBaseTest {

    @Test
    void testServerError() throws Exception {
        Project project = new Project();
        project.setProjectId(UUID.randomUUID());

        JSONObject obj = SafaRequest
            .withRoute(AppRoutes.Projects.Versions.GET_VERSIONS)
            .withProject(project)
            .getWithJsonObject(status().is4xxClientError());

        //Verification Points
        Object error = obj.get("message");
        assertThat(error).isNotNull();
    }
}
