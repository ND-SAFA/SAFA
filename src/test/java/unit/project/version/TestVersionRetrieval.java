package unit.project.version;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.common.AppRoutes;
import edu.nd.crc.safa.server.entities.db.Project;

import org.json.JSONArray;
import org.junit.jupiter.api.Test;
import unit.ApplicationBaseTest;

/**
 * Tests that users are able to retrieve a project versions.
 */
public class TestVersionRetrieval extends ApplicationBaseTest {
    @Test
    public void getEmptyVersions() throws Exception {
        Project project = dbEntityBuilder.newProjectWithReturn("test-project");
        JSONArray response = sendGetWithArrayResponse(createRouteName(project), status().isOk());
        assertThat(response.length()).isEqualTo(0);
    }

    @Test
    public void getMultipleVersions() throws Exception {
        String projectName = "test-project";
        dbEntityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .newVersion(projectName);
        Project project = dbEntityBuilder.getProject("test-project");
        JSONArray response = sendGetWithArrayResponse(createRouteName(project), status().isOk());
        assertThat(response.length()).isEqualTo(2);
    }

    private String createRouteName(Project project) {
        return RouteBuilder.withRoute(AppRoutes.Projects.Versions.getVersions).withProject(project).get();
    }
}
