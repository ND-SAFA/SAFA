package unit.project.parse;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.config.AppRoutes;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import unit.SampleProjectConstants;

/**
 * Tests that system is able to parse artifact and trace files containing no errors.
 */
public class TestArtifactAndTraceFileParse extends ParseBaseTest {

    /**
     * Tests that an artifact files contains as many artifacts as were defined within in.
     *
     * @throws Exception Throws exception if http request fail.
     */
    @Test
    public void testArtifactEntities() throws Exception {
        String baseRoute = AppRoutes.Projects.FlatFiles.parseArtifactFile;
        String routeName = RouteBuilder.withRoute(baseRoute).withArtifactType("Designs").get();
        String fileName = "Design.csv";

        //Step - Upload file, parse artifacts, and collect them
        JSONArray artifacts = uploadArtifactFileAndGetArtifacts(routeName, fileName);

        //VP - Verify that all artifacts were parsed
        assertThat(artifacts.length()).isEqualTo(SampleProjectConstants.N_DESIGNS);
    }

    /**
     * Tests that an traces files contains as many traces links  as were defined within in.
     *
     * @throws Exception Throws exception if http request fail.
     */
    @Test
    public void testTraceEntities() throws Exception {
        String fileName = "Design2Requirement.csv";

        // Step 1 - Upload TraceFile to parsing route and get response
        String route = AppRoutes.Projects.FlatFiles.parseTraceFile;
        JSONObject responseBody = parseFileAndReturnBody(route, fileName);

        // VP - Verify that message contains constraint
        JSONArray traces = responseBody.getJSONArray("traces");
        JSONArray errors = responseBody.getJSONArray("errors");
        assertThat(traces.length()).isGreaterThan(1);
        assertThat(errors.length()).isEqualTo(0);
    }
}
