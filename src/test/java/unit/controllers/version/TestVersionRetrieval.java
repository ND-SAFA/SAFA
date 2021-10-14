package unit.controllers.version;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import unit.EntityBaseTest;

public class TestVersionRetrieval extends EntityBaseTest {
    @Test
    public void getEmptyVersions() throws Exception {
        String projectId = entityBuilder
            .newProjectWithReturn("test-project").getProjectId().toString();
        JSONObject response = sendGet(createRouteName(projectId), status().isOk());
        assertThat(response.getJSONArray("body").length()).isEqualTo(0);
    }

    @Test
    public void getMultipleVersions() throws Exception {
        String projectName = "test-project";
        entityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .newVersion(projectName);
        String projectId = entityBuilder
            .getProject("test-project")
            .getProjectId()
            .toString();
        JSONObject response = sendGet(createRouteName(projectId), status().isOk());
        assertThat(response.getJSONArray("body").length()).isEqualTo(2);
    }

    private String createRouteName(String projectId) {
        return String.format("/projects/%s/versions", projectId);
    }
}
