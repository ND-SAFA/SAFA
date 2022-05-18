package unit.project.parse;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.config.AppRoutes;

import org.junit.jupiter.api.Test;
import unit.SampleProjectConstants;

public class TestParsingErrors extends ParseBaseTest {

    @Test
    public void errorForWrongColumnsInArtifactFile() throws Exception {
        String routeName = RouteBuilder.withRoute(AppRoutes.Projects.FlatFiles.parseArtifactFile).withArtifactType("Designs").get();
        String fileName = "Design2Requirement.csv";

        // VP - Verify error message informs that columns are wrong
        String c = uploadArtifactFileAndGetError(routeName, fileName);
        assertThat(c).contains("id, summary, content");
    }

    @Test
    public void errorForWrongColumnsInTraceFile() throws Exception {

        // VP - Verify error message informs that columns are wrong
        String c = uploadTraceFileAndGetError(AppRoutes.Projects.FlatFiles.parseTraceFile,
            SampleProjectConstants.DESIGN_FILE);
        assertThat(c).contains("source, target");
    }

    @Test
    public void errorForWrongFileToArtifactParser() throws Exception {
        String routeName = RouteBuilder.withRoute(AppRoutes.Projects.FlatFiles.parseArtifactFile).withArtifactType("Designs").get();
        String fileName = "tim.json";

        // VP - Verify error message informs that columns are wrong
        String c = uploadArtifactFileAndGetError(routeName, fileName);
        assertThat(c).contains("Expected a CSV file");
    }

    @Test
    public void errorForWrongFileToTraceParser() throws Exception {
        String fileName = "tim.json";

        // VP - Verify error message informs that columns are wrong
        String c = uploadTraceFileAndGetError(AppRoutes.Projects.FlatFiles.parseTraceFile, fileName);
        assertThat(c).contains("Expected a CSV file");
    }
}
