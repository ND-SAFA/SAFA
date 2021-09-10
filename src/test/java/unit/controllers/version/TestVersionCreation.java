package unit.controllers.version;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.db.entities.sql.Project;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import unit.EntityBaseTest;

public class TestVersionCreation extends EntityBaseTest {

    @Test
    public void attemptNewRevisionWithoutVersions() throws Exception {
        String projectName = "test-project";
        Project project = entityBuilder
            .newProjectWithReturn(projectName);
        String projectId = project
            .getProjectId()
            .toString();
        String routeName = String.format("/projects/%s/versions/revisions", projectId);
        JSONObject response = sendPost(routeName, new JSONObject(), status().is4xxClientError());
        assertThat(response.getJSONObject("body").getString("message")).contains("initial version");
    }

    @Test
    public void createFirstVersionThroughRevision() throws Exception {
        String projectName = "test-project";
        Project project = entityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .getProject(projectName);
        String projectId = project
            .getProjectId()
            .toString();
        String routeName = String.format("/projects/%s/versions/revisions", projectId);

        JSONObject response = sendPost(routeName, new JSONObject(), status().isCreated());
        JSONObject projectVersionJson = response.getJSONObject("body");

        assertThat(projectVersionJson.get("majorVersion")).isEqualTo(1);
        assertThat(projectVersionJson.get("minorVersion")).isEqualTo(1);
        assertThat(projectVersionJson.get("revision")).isEqualTo(2);
        assertThat(projectVersionJson.get("versionId")).isNotNull();

        this.projectVersionRepository.findByProject(project);
    }

    @Test
    public void createNewMinorVersion() throws Exception {
        String projectName = "test-project";
        Project project = entityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .getProject(projectName);
        String projectId = project
            .getProjectId()
            .toString();
        String routeName = String.format("/projects/%s/versions/minor", projectId);

        JSONObject response = sendPost(routeName, new JSONObject(), status().isCreated());
        JSONObject projectVersionJson = response.getJSONObject("body");

        assertThat(projectVersionJson.get("majorVersion")).isEqualTo(1);
        assertThat(projectVersionJson.get("minorVersion")).isEqualTo(2);
        assertThat(projectVersionJson.get("revision")).isEqualTo(1);
        assertThat(projectVersionJson.get("versionId")).isNotNull();

        this.projectVersionRepository.findByProject(project);
    }

    @Test
    public void createNewMajorVersion() throws Exception {
        String projectName = "test-project";
        Project project = entityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .getProject(projectName);
        String projectId = project
            .getProjectId()
            .toString();
        String routeName = String.format("/projects/%s/versions/major", projectId);

        JSONObject response = sendPost(routeName, new JSONObject(), status().isCreated());
        JSONObject projectVersionJson = response.getJSONObject("body");

        assertThat(projectVersionJson.get("majorVersion")).isEqualTo(2);
        assertThat(projectVersionJson.get("minorVersion")).isEqualTo(1);
        assertThat(projectVersionJson.get("revision")).isEqualTo(1);
        assertThat(projectVersionJson.get("versionId")).isNotNull();

        this.projectVersionRepository.findByProject(project);
    }
}
