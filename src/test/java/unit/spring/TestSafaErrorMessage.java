package unit.spring;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.UUID;

import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.db.Project;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import unit.ApplicationBaseTest;

/**
 * Tests that server errors include a
 * - status (0 if success otherwise some error code > 0)
 * - body (contains error message and other information)
 */
public class TestSafaErrorMessage extends ApplicationBaseTest {

    @Test
    public void testServerError() throws Exception {
        Project project = new Project();
        project.setProjectId(UUID.randomUUID());
        String routeName = RouteBuilder
            .withRoute(AppRoutes.Projects.getVersions)
            .withProject(project)
            .get();

        JSONObject obj = sendGet(routeName, status().isBadRequest());

        //Verification Points
        Integer responseStatus = (Integer) obj.get("status");

        assertThat(responseStatus).isNotNull();
        assertThat(responseStatus).isEqualTo(1);

        JSONObject body = obj.getJSONObject("body");
        assertThat(body).isNotNull();

        Object error = body.get("message");
        assertThat(error).isNotNull();
    }
}
