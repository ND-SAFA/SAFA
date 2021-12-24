package unit.flatfile;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.List;

import edu.nd.crc.safa.importer.flatfiles.ArtifactFileParser;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import unit.ApplicationBaseTest;
import unit.SampleProjectConstants;

/**
 * Provides smoke tests for testing the ArtifactFileParser
 */
public class TestArtifactFileParser extends ApplicationBaseTest {

    @Autowired
    ArtifactFileParser artifactFileParser;

    /**
     * Tests that a valid artifact file is read and converted to application entities.
     *
     * @throws Exception If any http requests fails.
     */
    @Test
    public void parseDesignArtifacts() throws Exception {
        ProjectVersion projectVersion = createProjectAndUploadBeforeFiles("testProject");

        // Step - parse Design artifact definition specification
        JSONObject jsonSpec = new JSONObject("{\n"
            + "    \"Design\": {\n"
            + "      \"file\": \"Design.csv\"\n"
            + "    }\n"
            + "  }");
        List<ArtifactAppEntity> artifacts = artifactFileParser.parseArtifactFiles(projectVersion, jsonSpec);

        // VP - Verify that all design artifacts are created
        assertThat(artifacts.size())
            .as("artifacts created")
            .isEqualTo(SampleProjectConstants.N_DESIGNS);
    }

    @Test
    public void missingFileKey() throws Exception {
        ProjectVersion projectVersion = createProjectAndUploadBeforeFiles("testProject");

        JSONObject jsonSpec = new JSONObject("{\n"
            + "    \"Design\": {}\n"
            + "  }");
        Exception exception = assertThrows(SafaError.class, () -> {
            artifactFileParser.parseArtifactFiles(projectVersion, jsonSpec);
        });
        assertThat(exception.getMessage()).contains("file");
        projectService.deleteProject(projectVersion.getProject());
    }
}
