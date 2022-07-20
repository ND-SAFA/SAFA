package unit.flatfile;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertThrows;

import edu.nd.crc.safa.common.EntityCreation;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.flatFiles.entities.TimParser;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import unit.ApplicationBaseTest;
import unit.SampleProjectConstants;

/**
 * Provides smoke tests for testing the ArtifactFileParser
 */
class TestArtifactFileParser extends ApplicationBaseTest {

    /**
     * Tests that a valid artifact file is read and converted to application entities.
     *
     * @throws Exception If any http requests fails.
     */
    @Test
    void parseDesignArtifacts() throws Exception {
        ProjectVersion projectVersion = createDefaultProject("testProject");

        // Step - parse Design artifact definition specification
        JSONObject jsonSpec = new JSONObject("{\"datafiles\": { \"Design\": {\"file\": \"Design.csv\"}}}");
        String pathToFiles = ProjectPaths.getPathToStorage(projectVersion.getProject());
        TimParser timParser = new TimParser(jsonSpec, pathToFiles);
        EntityCreation<ArtifactAppEntity, String> artifactCreationResponse = timParser.parseArtifacts();

        // VP - Verify that all design artifacts are created
        assertThat(artifactCreationResponse.getEntities().size())
            .as("artifacts created")
            .isEqualTo(SampleProjectConstants.N_DESIGNS);
    }

    @Test
    void missingFileKey() throws Exception {
        ProjectVersion projectVersion = createDefaultProject("testProject");

        JSONObject jsonSpec = new JSONObject("{\"datafiles\": { \"Design\": {}}}");
        String pathToFiles = ProjectPaths.getPathToUploadedFiles(projectVersion.getProject());
        Exception exception = assertThrows(SafaError.class, () -> new TimParser(jsonSpec, pathToFiles));
        assertThat(exception.getMessage()).contains("file");
        projectService.deleteProject(projectVersion.getProject());
    }
}
