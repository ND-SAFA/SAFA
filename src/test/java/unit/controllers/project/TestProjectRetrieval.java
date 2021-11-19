package unit.controllers.project;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.config.Routes;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import unit.ApplicationBaseTest;

public class TestProjectRetrieval extends ApplicationBaseTest {
    @Test
    public void getProjectsEmpty() throws Exception {
        JSONObject response = sendGet(Routes.getProjects, status().isOk());
        assertThat(response.getJSONArray("body").length()).isEqualTo(0);
    }

    @Test
    public void getProjectsMultiple() throws Exception {
        entityBuilder
            .newProject("firstProject")
            .newProject("secondProject");
        JSONObject response = sendGet(Routes.getProjects, status().isOk());
        assertThat(response.getJSONArray("body").length()).isEqualTo(2);
    }
}
