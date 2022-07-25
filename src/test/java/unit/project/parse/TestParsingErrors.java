package unit.project.parse;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.config.AppRoutes;

import org.junit.jupiter.api.Test;
import unit.DefaultProjectConstants;

class TestParsingErrors extends ParseBaseTest {

    @Test
    void errorForWrongColumnsInArtifactFile() throws Exception {
        String routeName = RouteBuilder
            .withRoute(AppRoutes.Projects.FlatFiles.parseArtifactFile)
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
        String c = uploadEntityFileAndGetError(AppRoutes.Projects.FlatFiles.parseTraceFile,
            DefaultProjectConstants.File.DESIGN_FILE);
        assertThat(c).contains("source, target");
    }

    @Test
    void jsonFileHasMissingArtifactKey() throws Exception {
        String routeName = RouteBuilder
            .withRoute(AppRoutes.Projects.FlatFiles.parseArtifactFile)
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
        String c = uploadEntityFileAndGetError(AppRoutes.Projects.FlatFiles.parseTraceFile, fileName);
        assertThat(c).contains("key").contains("traces");
    }
}
