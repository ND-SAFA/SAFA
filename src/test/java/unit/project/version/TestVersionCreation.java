package unit.project.version;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.db.Project;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import unit.ApplicationBaseTest;

/**
 * Tests that users are able to create new versions.
 */
public class TestVersionCreation extends ApplicationBaseTest {

    @Test
    public void attemptNewRevisionWithoutVersions() throws Exception {
        String projectName = "test-project";
        Project project = dbEntityBuilder
            .newProjectWithReturn(projectName);
        String routeName =
            RouteBuilder.withRoute(AppRoutes.Projects.Versions.createNewRevisionVersion).withProject(project).buildEndpoint();
        JSONObject response = sendPost(routeName, new JSONObject(), status().is4xxClientError());
        assertThat(response.getString("message")).contains("initial version");
    }

    @Test
    public void createFirstVersionThroughRevision() throws Exception {
        String projectName = "test-project";
        Project project = dbEntityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .getProject(projectName);
        String routeName =
            RouteBuilder.withRoute(AppRoutes.Projects.Versions.createNewRevisionVersion).withProject(project).buildEndpoint();
        JSONObject projectVersionJson = sendPost(routeName, new JSONObject(), status().isCreated());

        // VP - Verify that the correct version numbers appear
        assertThat(projectVersionJson.get("majorVersion")).isEqualTo(1);
        assertThat(projectVersionJson.get("minorVersion")).isEqualTo(1);
        assertThat(projectVersionJson.get("revision")).isEqualTo(2);
        assertThat(projectVersionJson.get("versionId")).isNotNull();

        this.projectVersionRepository.findByProject(project);
    }

    @Test
    public void createNewMinorVersion() throws Exception {
        String projectName = "test-project";
        Project project = dbEntityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .getProject(projectName);
        String routeName = RouteBuilder.withRoute(AppRoutes.Projects.Versions.createNewMinorVersion).withProject(project).buildEndpoint();

        JSONObject projectVersionJson = sendPost(routeName, new JSONObject(), status().isCreated());

        assertThat(projectVersionJson.get("majorVersion")).isEqualTo(1);
        assertThat(projectVersionJson.get("minorVersion")).isEqualTo(2);
        assertThat(projectVersionJson.get("revision")).isEqualTo(1);
        assertThat(projectVersionJson.get("versionId")).isNotNull();

        this.projectVersionRepository.findByProject(project);
    }

    @Test
    public void createNewMajorVersion() throws Exception {
        String projectName = "test-project";
        Project project = dbEntityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .getProject(projectName);
        String routeName = RouteBuilder.withRoute(AppRoutes.Projects.Versions.createNewMajorVersion).withProject(project).buildEndpoint();

        JSONObject projectVersionJson = sendPost(routeName, new JSONObject(), status().isCreated());

        assertThat(projectVersionJson.get("majorVersion")).isEqualTo(2);
        assertThat(projectVersionJson.get("minorVersion")).isEqualTo(1);
        assertThat(projectVersionJson.get("revision")).isEqualTo(1);
        assertThat(projectVersionJson.get("versionId")).isNotNull();

        this.projectVersionRepository.findByProject(project);
    }
}
