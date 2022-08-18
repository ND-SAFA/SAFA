package features.flatfiles.logic;

import static org.assertj.core.api.Assertions.assertThat;

import requests.RouteBuilder;

import edu.nd.crc.safa.config.AppRoutes;

import features.base.DefaultProjectConstants;
import features.flatfiles.base.ParseBaseTest;
import org.junit.jupiter.api.Test;

class TestParsingErrors extends ParseBaseTest {

    @Test
    void errorForWrongColumnsInArtifactFile() throws Exception {
        String routeName = RouteBuilder
            .withRoute(AppRoutes.FlatFiles.PARSE_ARTIFACT_FILE)
            .withArtifactType("Designs")
            .buildEndpoint();
        String fileName = "Design2Requirement.csv";

        // VP - Verify error message informs that columns are wrong
        String c = uploadEntityFileAndGetError(routeName, fileName);
        assertThat(c).contains("id, summary, content");
    }

    @Test
    void errorForWrongColumnsInTraceFile() throws Exception {
        // VP - Verify error message informs that columns are wrong
        String c = uploadEntityFileAndGetError(AppRoutes.FlatFiles.PARSE_TRACE_FILE,
            DefaultProjectConstants.File.DESIGN_FILE);
        assertThat(c).contains("source, target");
    }

    @Test
    void jsonFileHasMissingArtifactKey() throws Exception {
        String routeName = RouteBuilder
            .withRoute(AppRoutes.FlatFiles.PARSE_ARTIFACT_FILE)
            .withArtifactType("Designs")
            .buildEndpoint();
        String fileName = "tim.json";

        // VP - Verify error message informs that columns are wrong
        String c = uploadEntityFileAndGetError(routeName, fileName);
        assertThat(c).contains("key").contains("artifacts");
    }

    @Test
    void jsonFileHasMissingTraceKey() throws Exception {
        String fileName = "tim.json";

        // VP - Verify error message informs that columns are wrong
        String c = uploadEntityFileAndGetError(AppRoutes.FlatFiles.PARSE_TRACE_FILE, fileName);
        assertThat(c).contains("key").contains("traces");
    }
}
