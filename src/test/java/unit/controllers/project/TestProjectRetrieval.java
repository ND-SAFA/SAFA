package unit.controllers.project;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import unit.EntityBaseTest;

public class TestProjectRetrieval extends EntityBaseTest {
    @Test
    public void getProjectsEmpty() throws Exception {
        JSONObject response = sendGet("/projects/", status().isOk());
        assertThat(response.getJSONArray("body").length()).isEqualTo(0);
    }

    @Test
    public void getProjectsMultiple() throws Exception {
        entityBuilder
            .newProject("firstProject")
            .newProject("secondProject");
        JSONObject response = sendGet("/projects/", status().isOk());
        assertThat(response.getJSONArray("body").length()).isEqualTo(2);
    }
}
