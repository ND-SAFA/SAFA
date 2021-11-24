package unit.controllers.project.parse;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.config.AppRoutes;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.test.web.servlet.request.MockMultipartHttpServletRequestBuilder;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
import unit.ApplicationBaseTest;
import unit.TestConstants;

public class TestParseDataFilesErrors extends ApplicationBaseTest {

    @Test
    public void testDuplicateArtifact() throws Exception {

        // Step 1 - Upload flat files
        String routeName = RouteBuilder.withRoute(AppRoutes.parseArtifactFile).withArtifactType("designs").get();
        String pathToArtifactFile = ProjectPaths.PATH_TO_BEFORE_FILES + "/Design.csv";
        MockMultipartHttpServletRequestBuilder request = createSingleFileRequest(routeName, pathToArtifactFile);
        JSONObject responseContent = sendRequest(request, MockMvcResultMatchers.status().isOk(), this.token);

        // VP - Verify that no error occurred
        assertThat(responseContent.getInt("status")).isEqualTo(0);

        // VP - Verify that message contains constraint
        JSONObject body = responseContent.getJSONObject("body");
        JSONArray artifacts = body.getJSONArray("artifacts");
        JSONArray errors = body.getJSONArray("errors");
        assertThat(artifacts.length()).isEqualTo(TestConstants.N_DESIGNS);
        assertThat(errors.length()).isEqualTo(0);
    }

    @Test
    public void testParseTraceFile() throws Exception {

        // Step 1 - Upload flat files
        String routeName = RouteBuilder.withRoute(AppRoutes.parseTraceFile).get();
        MockMultipartHttpServletRequestBuilder request = createSingleFileRequest(routeName,
            ProjectPaths.PATH_TO_BEFORE_FILES + "/Design2Requirement.csv");
        JSONObject responseContent = sendRequest(request, MockMvcResultMatchers.status().isOk(), this.token);

        // VP - Verify that error occurred.
        assertThat(responseContent.getInt("status")).isEqualTo(0);

        // VP - Verify that message contains constraint
        JSONObject body = responseContent.getJSONObject("body");
        JSONArray traces = body.getJSONArray("traces");
        JSONArray errors = body.getJSONArray("errors");
        assertThat(traces.length()).isGreaterThan(1);
        assertThat(errors.length()).isEqualTo(0);
    }
}
