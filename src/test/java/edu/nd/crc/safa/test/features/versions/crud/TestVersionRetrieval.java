package edu.nd.crc.safa.test.features.versions.crud;

import static org.assertj.core.api.Assertions.assertThat;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.json.JSONArray;
import org.junit.jupiter.api.Test;

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
        dbEntityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .newVersion(projectName);
        Project project = dbEntityBuilder.getProject(projectName);
        JSONArray response = getVersionsInProject(project);
        assertThat(response.length()).isEqualTo(2);
    }

    private JSONArray getVersionsInProject(Project project) throws Exception {
        return new SafaRequest(AppRoutes.Versions.GET_VERSIONS)
            .withProject(project)
            .getWithJsonArray();
    }
}
