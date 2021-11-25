package unit.project.parse;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.config.AppRoutes;

import org.junit.jupiter.api.Test;

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
}
