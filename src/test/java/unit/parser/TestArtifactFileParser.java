package unit.parser;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.List;

import edu.nd.crc.safa.entities.Artifact;
import edu.nd.crc.safa.entities.Project;
import edu.nd.crc.safa.entities.ProjectVersion;
import edu.nd.crc.safa.flatfile.ArtifactFileParser;
import edu.nd.crc.safa.output.error.ServerError;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import unit.EntityBaseTest;
import unit.TestConstants;

public class TestArtifactFileParser extends EntityBaseTest {

    @Autowired
    ArtifactFileParser artifactFileParser;

    @Test
    public void parseDesignArtifacts() throws Exception {
        ProjectVersion projectVersion = createProjectWithTestResources("testProject");
        Project project = projectVersion.getProject();

        JSONObject jsonSpec = new JSONObject("{\n"
            + "    \"Design\": {\n"
            + "      \"file\": \"Design.csv\"\n"
            + "    }\n"
            + "  }");
        artifactFileParser.parseArtifactFiles(project, jsonSpec);

        List<Artifact> projectArtifacts = artifactRepository.findByProject(project);
        assertThat(projectArtifacts.size())
            .as("artifacts created")
            .isEqualTo(TestConstants.N_DESIGN_ARTIFACTS);
    }

    @Test
    public void missingFileKey() throws Exception {
        ProjectVersion projectVersion = createProjectWithTestResources("testProject");
        Project project = projectVersion.getProject();

        JSONObject jsonSpec = new JSONObject("{\n"
            + "    \"Design\": {}\n"
            + "  }");
        Exception exception = assertThrows(ServerError.class, () -> {
            artifactFileParser.parseArtifactFiles(project, jsonSpec);
        });
        assertThat(exception.getMessage()).contains("file");
    }
}
