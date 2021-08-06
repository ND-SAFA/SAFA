package unit.flatfile;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.List;

import edu.nd.crc.safa.entities.Artifact;
import edu.nd.crc.safa.entities.Project;
import edu.nd.crc.safa.entities.ProjectVersion;
import edu.nd.crc.safa.flatfiles.ArtifactFileParser;
import edu.nd.crc.safa.responses.ServerError;

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
        ProjectVersion projectVersion = createProjectUploadedResources("testProject");
        Project project = projectVersion.getProject();

        JSONObject jsonSpec = new JSONObject("{\n"
            + "    \"Design\": {\n"
            + "      \"file\": \"Design.csv\"\n"
            + "    }\n"
            + "  }");
        artifactFileParser.parseArtifactFiles(projectVersion, jsonSpec);

        List<Artifact> projectArtifacts = artifactRepository.findByProject(project);
        assertThat(projectArtifacts.size())
            .as("artifacts created")
            .isEqualTo(TestConstants.N_DESIGNS);
        projectService.deleteProject(project);
    }

    @Test
    public void missingFileKey() throws Exception {
        ProjectVersion projectVersion = createProjectUploadedResources("testProject");

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
