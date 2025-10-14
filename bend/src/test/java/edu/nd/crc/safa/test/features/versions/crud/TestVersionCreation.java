package edu.nd.crc.safa.test.features.versions.crud;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

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
        Project project = makeProject();
        JSONObject projectVersionJson = makeNewVersion(project, AppRoutes.Versions.CREATE_NEW_REVISION_VERSION);
        assertVersion(projectVersionJson, 1, 0, 1);
        this.projectVersionRepository.findByProject(project);
    }

    @Test
    void createNewMinorVersion() throws Exception {
        Project project = makeProject();
        JSONObject projectVersionJson = makeNewVersion(project, AppRoutes.Versions.CREATE_NEW_MINOR_VERSION);
        assertVersion(projectVersionJson, 1, 1, 0);
        this.projectVersionRepository.findByProject(project);
    }

    @Test
    void createNewMajorVersion() throws Exception {
        Project project = makeProject();
        JSONObject projectVersionJson = makeNewVersion(project, AppRoutes.Versions.CREATE_NEW_MAJOR_VERSION);
        assertVersion(projectVersionJson, 2, 0, 0);
        this.projectVersionRepository.findByProject(project);
    }

    @Test
    void testVersionReset() throws Exception {
        Project project = makeProject();

        JSONObject projectVersionJson = makeNewVersion(project, AppRoutes.Versions.CREATE_NEW_REVISION_VERSION);
        assertVersion(projectVersionJson, 1, 0, 1);

        projectVersionJson = makeNewVersion(project, AppRoutes.Versions.CREATE_NEW_MINOR_VERSION);
        assertVersion(projectVersionJson, 1, 1, 0);

        projectVersionJson = makeNewVersion(project, AppRoutes.Versions.CREATE_NEW_MAJOR_VERSION);
        assertVersion(projectVersionJson, 2, 0, 0);
        this.projectVersionRepository.findByProject(project);
    }

    private void assertVersion(JSONObject projectVersionJson, int majorVersion, int minorVersion, int revision) {
        assertThat(projectVersionJson.get("majorVersion")).isEqualTo(majorVersion);
        assertThat(projectVersionJson.get("minorVersion")).isEqualTo(minorVersion);
        assertThat(projectVersionJson.get("revision")).isEqualTo(revision);
        assertThat(projectVersionJson.get("versionId")).isNotNull();
    }

    private JSONObject makeNewVersion(Project project, String newVersionEndpoint) throws Exception {
        return SafaRequest
            .withRoute(newVersionEndpoint)
            .withProject(project)
            .postWithJsonObject(new JSONObject());
    }

    private Project makeProject() {
        return dbEntityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .getProject(projectName);
    }
}
