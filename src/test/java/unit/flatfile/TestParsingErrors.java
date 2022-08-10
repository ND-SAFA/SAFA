package unit.flatfile;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import edu.nd.crc.safa.builders.requests.SafaRequest;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.config.ProjectPaths;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
import unit.ApplicationBaseTest;

/**
 * Responsible for purposely occurring parsing errors and verifying that the correct
 * message is sent back.
 */
class TestParsingErrors extends ApplicationBaseTest {

    @Test
    void testArtifactTypeNotFound() throws Exception {

        // Step 1 - Upload flat files
        JSONObject responseBody = SafaRequest
            .withRoute(AppRoutes.Projects.FlatFiles.CREATE_NEW_PROJECT_FROM_FLAT_FILES)
            .getFlatFileHelper()
            .postWithFilesInDirectory(ProjectPaths.PATH_TO_TEST_2,
                MockMvcResultMatchers.status().isBadRequest(),
                new JSONObject());

        // VP - Verify that message contains constraint
        String message = responseBody.getString("message").toLowerCase();
        assertThat(message).matches("unknown artifact type: requirements");
    }

    @Test
    void testDuplicateArtifactBody() throws Exception {
        // Step 1 - Upload flat files
        JSONObject responseBody = SafaRequest
            .withRoute(AppRoutes.Projects.FlatFiles.CREATE_NEW_PROJECT_FROM_FLAT_FILES)
            .getFlatFileHelper()
            .postWithFilesInDirectory(ProjectPaths.PATH_TO_TEST_3, new JSONObject());
        // VP - Verify that message contains artifact that failed constraint
        JSONObject errors = responseBody.getJSONObject("errors");
        JSONArray artifactErrors = errors.getJSONArray("artifacts");
        assertThat(artifactErrors.length()).isEqualTo(1);

        // VP - Verify that artifact error specifies which artifact it occurred on.
        String artifactError = artifactErrors.getJSONObject(0).getString("message").toLowerCase();
        assertThat(artifactError).matches(".*duplicate.*artifact.*saf4.*");
    }
}
