package unit.controllers.project.parse;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.config.ProjectPaths;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.test.web.servlet.request.MockMultipartHttpServletRequestBuilder;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;

public class TestParsingErrors extends ParseBaseTest {

    @Test
    public void errorForWrongColumnsInArtifactFile() throws Exception {
        String routeName = RouteBuilder.withRoute(AppRoutes.parseArtifactFile).withArtifactType("Designs").get();
        String fileName = "Design2Requirement.csv";

        // VP - Verify error message informs that columns are wrong
        String c = uploadArtifactFileAndGetError(routeName, fileName);
        assertThat(c).contains("id, summary, content");
    }

    @Test
    public void errorForWrongColumnsInTraceFile() throws Exception {
        String fileName = "Design.csv";

        // VP - Verify error message informs that columns are wrong
        String c = uploadTraceFileAndGetError(AppRoutes.parseTraceFile, fileName);
        assertThat(c).contains("source, target");
    }

    @Test
    public void errorForWrongFileToArtifactParser() throws Exception {
        String routeName = RouteBuilder.withRoute(AppRoutes.parseArtifactFile).withArtifactType("Designs").get();
        String fileName = "tim.json";

        // VP - Verify error message informs that columns are wrong
        String c = uploadArtifactFileAndGetError(routeName, fileName);
        assertThat(c).contains("Expected a CSV file");
    }

    @Test
    public void errorForWrongFileToTraceParser() throws Exception {
        String fileName = "tim.json";

        // VP - Verify error message informs that columns are wrong
        String c = uploadTraceFileAndGetError(AppRoutes.parseTraceFile, fileName);
        assertThat(c).contains("Expected a CSV file");
    }


    private String uploadArtifactFileAndGetError(String routeName, String fileName) throws Exception {
        return uploadEntityFileAndGetError(routeName, fileName, "artifacts");
    }

    private String uploadTraceFileAndGetError(String routeName, String fileName) throws Exception {
        return uploadEntityFileAndGetError(routeName, fileName, "traces");
    }

    private String uploadEntityFileAndGetError(String routeName, String fileName, String entityName) throws Exception {
        // Step - Upload file and get response body
        JSONObject body = uploadFileAndGetBody(routeName, fileName);

        // Step - Extract artifact and errors from body
        JSONArray entities = body.getJSONArray(entityName);
        JSONArray errors = body.getJSONArray("errors");

        // VP - Verify that message contains constraint
        assertThat(entities.length()).isEqualTo(0);
        assertThat(errors.length()).isEqualTo(1);

        return errors.getString(0);
    }

    private JSONArray uploadArtifactFileAndGetArtifacts(String routeName, String fileName) throws Exception {
        // Step - Upload file and get response body
        JSONObject body = uploadFileAndGetBody(routeName, fileName);

        // Step - Extract artifact and errors from body
        JSONArray artifacts = body.getJSONArray("artifacts");
        JSONArray errors = body.getJSONArray("errors");

        // VP - Verify that message contains constraint
        assertThat(errors.length()).isEqualTo(0);

        return artifacts;
    }

    private JSONObject uploadFileAndGetBody(String routeName, String fileName) throws Exception {
        // Step - Upload flat files
        MockMultipartHttpServletRequestBuilder request = createSingleFileRequest(routeName,
            ProjectPaths.PATH_TO_BEFORE_FILES + "/" + fileName);
        JSONObject responseContent = sendRequest(request, MockMvcResultMatchers.status().isOk(), this.token);

        // VP - Verify that error occurred.
        assertThat(responseContent.getInt("status")).isEqualTo(0);

        // Step - Extract artifact and errors from body
        return responseContent.getJSONObject("body");
    }
}
