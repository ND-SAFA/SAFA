package unit.flatfile;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertThrows;

import edu.nd.crc.safa.common.EntityCreation;
import edu.nd.crc.safa.importer.flatfiles.ArtifactFileParser;
import edu.nd.crc.safa.importer.flatfiles.TIMParser;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;
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
        JSONObject jsonSpec = new JSONObject("{\"datafiles\": { \"Design\": {\"file\": \"Design.csv\"}}}");
        TIMParser TIMParser = new TIMParser(jsonSpec);
        TIMParser.parse();
        EntityCreation<ArtifactAppEntity, String> artifactCreationResponse =
            artifactFileParser.parseArtifactFiles(projectVersion,
                TIMParser);

        // VP - Verify that all design artifacts are created
        assertThat(artifactCreationResponse.getEntities().size())
            .as("artifacts created")
            .isEqualTo(SampleProjectConstants.N_DESIGNS);
    }

    @Test
    public void missingFileKey() throws Exception {
        ProjectVersion projectVersion = createProjectAndUploadBeforeFiles("testProject");

        JSONObject jsonSpec = new JSONObject("{\"datafiles\": { \"Design\": {}}}");

        TIMParser TIMParser = new TIMParser(jsonSpec);

        Exception exception = assertThrows(SafaError.class, TIMParser::parse);
        assertThat(exception.getMessage()).contains("file");
        projectService.deleteProject(projectVersion.getProject());
    }
}
