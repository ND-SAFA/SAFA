package edu.nd.crc.safa.test.features.flatfiles.logic;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertThrows;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.common.EntityParsingResult;
import edu.nd.crc.safa.features.flatfiles.parser.FlatFileParser;
import edu.nd.crc.safa.features.flatfiles.parser.TimFileParser;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.common.DefaultProjectConstants;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;

/**
 * Provides smoke tests for testing the ArtifactFileParser
 */
class TestArtifactIFileParser extends ApplicationBaseTest {

    /**
     * Tests that a valid artifact file is read and converted to application entities.
     *
     * @throws Exception If any http requests fails.
     */
    @Test
    void parseDesignArtifacts() throws Exception {
        ProjectVersion projectVersion = creationService.uploadDefaultProject("testProject");

        // Step - parse Design artifact definition specification
        JSONObject jsonSpec
            = new JSONObject("{\"artifacts\":[{\"type\": \"Design\", \"fileName\": \"Design.csv\"}], \"traces\": []}");
        String pathToFiles = ProjectPaths.Storage.projectUploadsPath(projectVersion.getProject(), false);
        TimFileParser timFileParser = new TimFileParser(jsonSpec, pathToFiles);
        FlatFileParser flatFileParser = new FlatFileParser(timFileParser);
        EntityParsingResult<ArtifactAppEntity, String> artifactCreationResponse = flatFileParser.parseArtifacts();

        // VP - Verify that all design artifacts are created
        assertThat(artifactCreationResponse.getEntities())
            .as("artifacts created")
            .hasSize(DefaultProjectConstants.Entities.N_DESIGNS);
    }

    @Test
    void missingFileKey() throws Exception {
        ProjectVersion projectVersion = creationService.uploadDefaultProject("testProject");
        JSONObject jsonSpec = new JSONObject("{\"artifacts\":[{\"type\": \"Design\"}]}");
        String pathToFiles = ProjectPaths.Storage.projectUploadsPath(projectVersion.getProject(), false);
        TimFileParser timFileParser = new TimFileParser(jsonSpec, pathToFiles);
        Exception exception = assertThrows(SafaError.class, () -> new FlatFileParser(timFileParser));
        assertThat(exception.getMessage()).contains("file");
        projectService.deleteProject(getCurrentUser(), projectVersion.getProject());
    }
}
