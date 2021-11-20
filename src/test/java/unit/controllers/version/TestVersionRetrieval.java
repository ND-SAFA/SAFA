package unit.controllers.version;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.config.Routes;
import edu.nd.crc.safa.server.entities.db.Project;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import unit.ApplicationBaseTest;

public class TestVersionRetrieval extends ApplicationBaseTest {
    @Test
    public void getEmptyVersions() throws Exception {
        Project project = entityBuilder.newProjectWithReturn("test-project");
        JSONObject response = sendGet(createRouteName(project), status().isOk());
        assertThat(response.getJSONArray("body").length()).isEqualTo(0);
    }

    @Test
    public void getMultipleVersions() throws Exception {
        String projectName = "test-project";
        entityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .newVersion(projectName);
        Project project = entityBuilder.getProject("test-project");
        JSONObject response = sendGet(createRouteName(project), status().isOk());
        assertThat(response.getJSONArray("body").length()).isEqualTo(2);
    }

    private String createRouteName(Project project) {
        return RouteBuilder.withRoute(Routes.getVersions).withProject(project).get();
    }
}
