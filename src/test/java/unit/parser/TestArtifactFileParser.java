package unit.parser;

import edu.nd.crc.safa.entities.ArtifactType;
import edu.nd.crc.safa.entities.Project;
import edu.nd.crc.safa.entities.ProjectVersion;
import edu.nd.crc.safa.flatfile.ArtifactFileParser;

import org.json.JSONObject;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import unit.EntityBaseTest;

public class TestArtifactFileParser extends EntityBaseTest {

    @Autowired
    ArtifactFileParser artifactFileParser;

    @Test
    @Disabled
    public void parseExample() throws Exception {
        ProjectVersion projectVersion = createProjectWithTestResources("testProject");
        Project project = projectVersion.getProject();

        ArtifactType artifactType = createArtifactType(project, "Design");
        JSONObject jsonSpec = new JSONObject("{\n"
            + "    \"Design\": {\n"
            + "      \"file\": \"Design.csv\"\n"
            + "    }\n"
            + "  }");
        artifactFileParser.parseArtifactFiles(project, jsonSpec);
    }
}
