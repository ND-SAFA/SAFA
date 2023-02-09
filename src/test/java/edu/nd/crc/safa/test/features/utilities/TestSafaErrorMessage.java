package edu.nd.crc.safa.test.features.utilities;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.UUID;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;

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
            .withRoute(AppRoutes.Versions.GET_VERSIONS)
            .withProject(project)
            .getWithJsonObject(status().is4xxClientError());

        //Verification Points
        Object error = obj.get("message");
        assertThat(error).isNotNull();
    }
}
