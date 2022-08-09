package unit.project.parse;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import edu.nd.crc.safa.builders.requests.SafaRequest;
import edu.nd.crc.safa.config.ProjectPaths;

import org.json.JSONArray;
import org.json.JSONObject;
import unit.ApplicationBaseTest;

/**
 * Provides a base of functions for testing the parsing of data files.
 */
public abstract class ParseBaseTest extends ApplicationBaseTest {

    public String uploadEntityFileAndGetError(String routeName, String fileName) throws Exception {
        // Step - Upload file and get response body
        JSONObject body = parseFileAndReturnBody(routeName, fileName);

        // Step - Extract artifact and errors from body
        JSONArray entities = body.getJSONArray("entities");
        JSONArray errors = body.getJSONArray("errors");

        // VP - Verify that message contains constraint
        assertThat(entities.length()).isZero();
        assertThat(errors.length()).isEqualTo(1);

        return errors.getString(0);
    }

    protected JSONArray uploadFileAndGetEntities(String routeName) throws Exception {
        // Step - Upload file and get response body
        JSONObject body = parseFileAndReturnBody(routeName, unit.DefaultProjectConstants.File.DESIGN_FILE);

        // Step - Extract artifact and errors from body
        JSONArray entities = body.getJSONArray("entities");
        JSONArray errors = body.getJSONArray("errors");

        // VP - Verify that message contains constraint
        assertThat(errors.length()).isZero();

        return entities;
    }

    protected JSONObject parseFileAndReturnBody(String routeName, String fileName) throws Exception {
        // Step - Upload flat files
        String pathToFile = ProjectPaths.getPathToDefaultProjectFile(fileName);
        return SafaRequest
            .withRoute(routeName)
            .getFlatFileHelper()
            .postWithFile(pathToFile);
    }
}
