package unit.project.parse;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import edu.nd.crc.safa.config.ProjectPaths;

import org.json.JSONArray;
import org.json.JSONObject;
import org.springframework.test.web.servlet.request.MockMultipartHttpServletRequestBuilder;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
import unit.ApplicationBaseTest;

/**
 * Provides a base of functions for testing the parsing of data files.
 */
public class ParseBaseTest extends ApplicationBaseTest {

    protected String uploadArtifactFileAndGetError(String routeName, String fileName) throws Exception {
        return uploadEntityFileAndGetError(routeName, fileName, "artifacts");
    }

    protected String uploadTraceFileAndGetError(String routeName, String fileName) throws Exception {
        return uploadEntityFileAndGetError(routeName, fileName, "traces");
    }

    protected String uploadEntityFileAndGetError(String routeName, String fileName, String entityName) throws Exception {
        // Step - Upload file and get response body
        JSONObject body = parseFileAndReturnBody(routeName, fileName);

        // Step - Extract artifact and errors from body
        JSONArray entities = body.getJSONArray(entityName);
        JSONArray errors = body.getJSONArray("errors");

        // VP - Verify that message contains constraint
        assertThat(entities.length()).isEqualTo(0);
        assertThat(errors.length()).isEqualTo(1);

        return errors.getString(0);
    }

    protected JSONArray uploadArtifactFileAndGetArtifacts(String routeName, String fileName) throws Exception {
        // Step - Upload file and get response body
        JSONObject body = parseFileAndReturnBody(routeName, fileName);

        // Step - Extract artifact and errors from body
        JSONArray artifacts = body.getJSONArray("artifacts");
        JSONArray errors = body.getJSONArray("errors");

        // VP - Verify that message contains constraint
        assertThat(errors.length()).isEqualTo(0);

        return artifacts;
    }

    protected JSONObject parseFileAndReturnBody(String routeName, String fileName) throws Exception {
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
