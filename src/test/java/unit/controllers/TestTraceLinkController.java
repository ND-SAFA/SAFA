package unit.controllers;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
import unit.EntityBaseTest;

public class TestTraceLinkController extends EntityBaseTest {

    @Test
    public void testGetGeneratedLinks() throws Exception {
        String projectName = "test-project";
        String sourceName = "RE-8";
        String targetName = "DD-10";
        double score = 0.2;

        entityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .newType(projectName, "A")
            .newType(projectName, "B")
            .newArtifact(projectName, "A", sourceName)
            .newArtifact(projectName, "B", targetName)
            .newGeneratedTraceLink(projectName, sourceName, targetName, score);

        String projectId = entityBuilder.getProject(projectName).getProjectId().toString();
        String url = String.format("/projects/%s/links/generated", projectId);
        JSONObject response = sendGet(url, MockMvcResultMatchers.status().isOk());
        JSONArray links = response.getJSONArray("body");
        assertThat(links.length()).isEqualTo(1);
        assertThat(links.getJSONObject(0).getString("source")).isEqualTo(sourceName);
        assertThat(links.getJSONObject(0).getString("target")).isEqualTo(targetName);
    }
}
