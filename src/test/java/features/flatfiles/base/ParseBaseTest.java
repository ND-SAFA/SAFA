package features.flatfiles.base;

import static org.assertj.core.api.Assertions.assertThat;

import requests.SafaRequest;

import edu.nd.crc.safa.config.ProjectPaths;

import features.base.ApplicationBaseTest;
import features.base.DefaultProjectConstants;
import org.json.JSONArray;
import org.json.JSONObject;

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
        JSONObject body = parseFileAndReturnBody(routeName, DefaultProjectConstants.File.DESIGN_FILE);

        // Step - Extract artifact and errors from body
        JSONArray entities = body.getJSONArray("entities");
        JSONArray errors = body.getJSONArray("errors");

        // VP - Verify that message contains constraint
        assertThat(errors.length()).isZero();

        return entities;
    }

    protected JSONObject parseFileAndReturnBody(String routeName, String fileName) throws Exception {
        // Step - Upload flat files
        String pathToFile = ProjectPaths.Tests.DefaultProject.getPathToFile(fileName);
        return SafaRequest
            .withRoute(routeName)
            .getFlatFileHelper()
            .postWithFile(pathToFile);
    }
}
