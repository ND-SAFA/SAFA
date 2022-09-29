package features.versions.crud;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import requests.SafaRequest;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.projects.entities.db.Project;

import common.ApplicationBaseTest;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;

/**
 * Tests that users are able to create new versions.
 */
class TestVersionCreation extends ApplicationBaseTest {

    @Test
    void attemptNewRevisionWithoutVersions() throws Exception {
        Project project = dbEntityBuilder
            .newProjectWithReturn(projectName);
        JSONObject response =
            SafaRequest
                .withRoute(AppRoutes.Versions.CREATE_NEW_REVISION_VERSION)
                .withProject(project)
                .postWithJsonObject(new JSONObject(), status().is4xxClientError());
        assertThat(response.getString("message")).contains("initial version");
    }

    @Test
    void createFirstVersionThroughRevision() throws Exception {
        Project project = dbEntityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .getProject(projectName);
        JSONObject projectVersionJson =
            SafaRequest
                .withRoute(AppRoutes.Versions.CREATE_NEW_REVISION_VERSION)
                .withProject(project)
                .postWithJsonObject(new JSONObject());

        // VP - Verify that the correct version numbers appear
        assertThat(projectVersionJson.get("majorVersion")).isEqualTo(1);
        assertThat(projectVersionJson.get("minorVersion")).isEqualTo(1);
        assertThat(projectVersionJson.get("revision")).isEqualTo(2);
        assertThat(projectVersionJson.get("versionId")).isNotNull();

        this.projectVersionRepository.findByProject(project);
    }

    @Test
    void createNewMinorVersion() throws Exception {
        Project project = dbEntityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .getProject(projectName);
        JSONObject projectVersionJson = SafaRequest
            .withRoute(AppRoutes.Versions.CREATE_NEW_MINOR_VERSION)
            .withProject(project)
            .postWithJsonObject(new JSONObject());

        assertThat(projectVersionJson.get("majorVersion")).isEqualTo(1);
        assertThat(projectVersionJson.get("minorVersion")).isEqualTo(2);
        assertThat(projectVersionJson.get("revision")).isEqualTo(1);
        assertThat(projectVersionJson.get("versionId")).isNotNull();

        this.projectVersionRepository.findByProject(project);
    }

    @Test
    void createNewMajorVersion() throws Exception {
        Project project = dbEntityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .getProject(projectName);
        JSONObject projectVersionJson = SafaRequest
            .withRoute(AppRoutes.Versions.CREATE_NEW_MAJOR_VERSION)
            .withProject(project)
            .postWithJsonObject(new JSONObject());

        assertThat(projectVersionJson.get("majorVersion")).isEqualTo(2);
        assertThat(projectVersionJson.get("minorVersion")).isEqualTo(1);
        assertThat(projectVersionJson.get("revision")).isEqualTo(1);
        assertThat(projectVersionJson.get("versionId")).isNotNull();

        this.projectVersionRepository.findByProject(project);
    }
}
