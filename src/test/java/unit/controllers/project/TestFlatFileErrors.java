package unit.controllers.project;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import edu.nd.crc.safa.config.ProjectPaths;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.test.web.servlet.request.MockMultipartHttpServletRequestBuilder;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
import unit.ApplicationBaseTest;

public class TestFlatFileErrors extends ApplicationBaseTest {

    @Test
    public void testArtifactTypeNotFound() throws Exception {

        // Step 1 - Upload flat files
        String routeName = "/projects/flat-files";
        MockMultipartHttpServletRequestBuilder request = createMultiPartRequest(routeName,
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
        String routeName = "/projects/flat-files";
        MockMultipartHttpServletRequestBuilder request = createMultiPartRequest(routeName,
            ProjectPaths.PATH_TO_TEST_3);
        JSONObject responseContent = sendRequest(request, MockMvcResultMatchers.status().isBadRequest(), this.token);

        // VP - Verify that error occurred.
        assertThat(responseContent.getInt("status")).isEqualTo(1);

        // VP - Verify that message contains artifact that failed constraint
        JSONObject body = responseContent.getJSONObject("body");
        String message = body.getString("message");
        assertThat(message).contains("SAF4");

        // VP - Verify that details contain constraint name
        String details = body.getString("details");
        assertThat(details).contains("UNIQUE_ARTIFACT_BODY_PER_VERSION");
    }
}
