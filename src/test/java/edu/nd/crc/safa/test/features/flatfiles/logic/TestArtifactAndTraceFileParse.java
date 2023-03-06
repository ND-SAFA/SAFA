package edu.nd.crc.safa.test.features.flatfiles.logic;

import static org.assertj.core.api.Assertions.assertThat;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.test.common.DefaultProjectConstants;
import edu.nd.crc.safa.test.features.flatfiles.base.ParseBaseTest;
import edu.nd.crc.safa.test.requests.RouteBuilder;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;

/**
 * Tests that system is able to parse artifact and trace files containing no errors.
 */
class TestArtifactAndTraceFileParse extends ParseBaseTest {

    /**
     * Tests that an artifact files contains as many artifacts as were defined within in.
     *
     * @throws Exception Throws exception if http request fail.
     */
    @Test
    void testArtifactEntities() throws Exception {
        String baseRoute = AppRoutes.FlatFiles.PARSE_ARTIFACT_FILE;
        String type = "Design";

        //Step - Upload file, parse artifacts, and collect them
        String routeName = RouteBuilder.withRoute(baseRoute).withArtifactType(type).buildEndpoint();
        JSONArray artifacts = uploadFileAndGetEntities(routeName);

        //VP - Verify that all artifacts were parsed
        assertThat(artifacts.length()).isEqualTo(DefaultProjectConstants.Entities.N_DESIGNS);

        for (int i = 0; i < artifacts.length(); i++) {
            JSONObject artifact = artifacts.getJSONObject(i);
            assertThat(artifact.getString("type")).isEqualTo(type);
        }
    }

    /**
     * Tests that an traces files contains as many traces links  as were defined within in.
     *
     * @throws Exception Throws exception if http request fail.
     */
    @Test
    void testTraceEntities() throws Exception {
        String fileName = "Design2Requirement.csv";

        // Step 1 - Upload TraceFile to parsing route and get response
        String route = AppRoutes.FlatFiles.PARSE_TRACE_FILE;
        JSONObject responseBody = parseFileAndReturnBody(route, fileName);

        // VP - Verify that message contains constraint
        JSONArray traces = responseBody.getJSONArray("entities");
        JSONArray errors = responseBody.getJSONArray("errors");
        assertThat(traces.length()).isGreaterThan(1);
        assertThat(errors.length()).isZero();
    }
}
