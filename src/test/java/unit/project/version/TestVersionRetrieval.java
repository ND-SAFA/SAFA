package unit.project.version;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import edu.nd.crc.safa.builders.requests.SafaRequest;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.db.Project;

import org.json.JSONArray;
import org.junit.jupiter.api.Test;
import unit.ApplicationBaseTest;

/**
 * Tests that users are able to retrieve a project versions.
 */
class TestVersionRetrieval extends ApplicationBaseTest {
    @Test
    void getEmptyVersions() throws Exception {
        Project project = dbEntityBuilder.newProjectWithReturn("test-project");
        JSONArray response = getVersionsInProject(project);
        assertThat(response.length()).isZero();
    }

    @Test
    void getMultipleVersions() throws Exception {
        String projectName = "test-project";
        dbEntityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .newVersion(projectName);
        Project project = dbEntityBuilder.getProject("test-project");
        JSONArray response = getVersionsInProject(project);
        assertThat(response.length()).isEqualTo(2);
    }

    private JSONArray getVersionsInProject(Project project) throws Exception {
        return new SafaRequest(AppRoutes.Projects.Versions.GET_VERSIONS)
            .withProject(project)
            .getWithJsonArray();
    }
}
