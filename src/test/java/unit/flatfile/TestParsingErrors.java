package unit.flatfile;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.config.ProjectPaths;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.test.web.servlet.request.MockMultipartHttpServletRequestBuilder;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
import unit.ApplicationBaseTest;

/**
 * Responsible for purposely occurring parsing errors and verifying that the correct
 * message is sent back.
 */
public class TestParsingErrors extends ApplicationBaseTest {

    @Test
    public void testArtifactTypeNotFound() throws Exception {

        // Step 1 - Upload flat files
        MockMultipartHttpServletRequestBuilder request = createMultiPartRequest(AppRoutes.projectFlatFiles,
            ProjectPaths.PATH_TO_TEST_2);
        JSONObject responseContent = sendRequest(request, MockMvcResultMatchers.status().isBadRequest(), this.token);

        // VP - Verify that error occurred.
        assertThat(responseContent.getInt("status")).isEqualTo(1);

        // VP - Verify that message contains constraint
        JSONObject body = responseContent.getJSONObject("body");
        String message = body.getString("message");
        assertThat(message).contains("Unexpected artifact type: Requirements");
    }

    @Test
    public void testDuplicateArtifactBody() throws Exception {

        // Step 1 - Upload flat files
        MockMultipartHttpServletRequestBuilder request = createMultiPartRequest(AppRoutes.projectFlatFiles,
            ProjectPaths.PATH_TO_TEST_3);
        JSONObject responseContent = sendRequest(request, MockMvcResultMatchers.status().is2xxSuccessful(), this.token);

        // VP - Verify that error occurred.
        assertThat(responseContent.getInt("status")).isEqualTo(0);

        // VP - Verify that message contains artifact that failed constraint
        JSONObject errors = responseContent.getJSONObject("body").getJSONObject("errors");
        JSONArray artifactErrors = errors.getJSONArray("artifacts");
        assertThat(artifactErrors.length()).isEqualTo(1);

        // VP - Verify that artifact error specifies which artifact it occurred on.
        String artifactError = artifactErrors.getJSONObject(0).getString("message");
        assertThat(artifactError).matches(".*SAF4.*artifact.*name.*[\\s\\S]");
    }
}
