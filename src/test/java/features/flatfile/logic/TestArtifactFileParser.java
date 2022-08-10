package features.flatfile.logic;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertThrows;

import edu.nd.crc.safa.common.EntityParsingResult;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.flatfiles.entities.FlatFileParser;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import features.base.ApplicationBaseTest;
import features.base.DefaultProjectConstants;

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
        String pathToFiles = ProjectPaths.getPathToUploadedFiles(projectVersion.getProject(), false);
        FlatFileParser flatFileParser = new FlatFileParser(jsonSpec, pathToFiles);
        EntityParsingResult<ArtifactAppEntity, String> artifactCreationResponse = flatFileParser.parseArtifacts();

        // VP - Verify that all design artifacts are created
        assertThat(artifactCreationResponse.getEntities().size())
            .as("artifacts created")
            .isEqualTo(DefaultProjectConstants.Entities.N_DESIGNS);
    }

    @Test
    void missingFileKey() throws Exception {
        ProjectVersion projectVersion = createDefaultProject("testProject");

        JSONObject jsonSpec = new JSONObject("{\"datafiles\": { \"Design\": {}}}");
        String pathToFiles = ProjectPaths.getPathToUploadedFiles(projectVersion.getProject(), false);
        Exception exception = assertThrows(SafaError.class, () -> new FlatFileParser(jsonSpec, pathToFiles));
        assertThat(exception.getMessage()).contains("file");
        projectService.deleteProject(projectVersion.getProject());
    }
}
