package edu.nd.crc.safa.test.features.flatfiles.logic;

import static org.assertj.core.api.Assertions.assertThat;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;

/**
 * Responsible for purposely occurring parsing errors and verifying that the correct
 * message is sent back.
 */
class TestArtifactFileParsingErrors extends ApplicationBaseTest {

    @Test
    void testArtifactTypeNotFound() throws Exception {
        dbEntityBuilder.newProject(projectName);
        ProjectVersion version = dbEntityBuilder.newVersionWithReturn(projectName);

        // Step 1 - Upload flat files
        JSONObject responseBody = SafaRequest
            .withRoute(AppRoutes.FlatFiles.UPDATE_PROJECT_VERSION_FROM_FLAT_FILES)
            .withVersion(version)
            .getFlatFileHelper()
            .postWithFilesInDirectory(ProjectPaths.Resources.Tests.TEST2,
                MockMvcResultMatchers.status().isBadRequest(),
                new JSONObject());

        // VP - Verify that message contains constraint
        String message = responseBody.getString("message").toLowerCase();
        assertThat(message).contains("unknown artifact type: requirements");
    }

    @Test
    void testDuplicateArtifactBody() throws Exception {
        dbEntityBuilder.newProject(projectName);
        ProjectVersion version = dbEntityBuilder.newVersionWithReturn(projectName);

        // Step 1 - Upload flat files
        JSONObject responseBody = SafaRequest
            .withRoute(AppRoutes.FlatFiles.UPDATE_PROJECT_VERSION_FROM_FLAT_FILES)
            .withVersion(version)
            .getFlatFileHelper()
            .postWithFilesInDirectory(ProjectPaths.Resources.Tests.TEST3, new JSONObject());

        // VP - Verify that message contains artifact that failed constraint
        JSONObject errors = responseBody.getJSONObject("errors");
        JSONArray artifactErrors = errors.getJSONArray("artifacts");
        assertThat(artifactErrors.length()).isEqualTo(1);

        // VP - Verify that artifact error specifies which artifact it occurred on.
        String artifactError = artifactErrors.getJSONObject(0).getString("message").toLowerCase();
        assertThat(artifactError).matches(".*duplicate.*artifact.*saf4.*");
    }
}
