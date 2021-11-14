package unit.flatfile;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.List;

import edu.nd.crc.safa.importer.flatfiles.ArtifactFileParser;
import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.api.ServerError;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import unit.EntityBaseTest;
import unit.TestConstants;

public class TestArtifactNodeFileParser extends EntityBaseTest {

    @Autowired
    ArtifactFileParser artifactFileParser;

    @Test
    public void parseDesignArtifacts() throws Exception {
        ProjectVersion projectVersion = createProjectAndUploadBeforeFiles("testProject");
        Project project = projectVersion.getProject();

        // Step - parse Design artifact definition specification
        JSONObject jsonSpec = new JSONObject("{\n"
            + "    \"Design\": {\n"
            + "      \"file\": \"Design.csv\"\n"
            + "    }\n"
            + "  }");
        artifactFileParser.parseArtifactFiles(projectVersion, jsonSpec);

        // VP - Verify that all design artifacts are created
        List<Artifact> projectArtifacts = artifactRepository.getProjectArtifacts(project);
        assertThat(projectArtifacts.size())
            .as("artifacts created")
            .isEqualTo(TestConstants.N_DESIGNS);
        projectService.deleteProject(project);
    }

    @Test
    public void missingFileKey() throws Exception {
        ProjectVersion projectVersion = createProjectAndUploadBeforeFiles("testProject");

        JSONObject jsonSpec = new JSONObject("{\n"
            + "    \"Design\": {}\n"
            + "  }");
        Exception exception = assertThrows(ServerError.class, () -> {
            artifactFileParser.parseArtifactFiles(projectVersion, jsonSpec);
        });
        assertThat(exception.getMessage()).contains("file");
        projectService.deleteProject(projectVersion.getProject());
    }
}
