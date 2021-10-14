package unit.flatfile;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.io.IOException;

import edu.nd.crc.safa.importer.flatfiles.TraceFileParser;
import edu.nd.crc.safa.server.db.entities.sql.ArtifactType;
import edu.nd.crc.safa.server.db.entities.sql.Project;
import edu.nd.crc.safa.server.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.server.messages.ServerError;

import org.javatuples.Pair;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import unit.EntityBaseTest;

public class TestTraceFileParser extends EntityBaseTest {

    @Autowired
    TraceFileParser traceFileParser;

    String jsonString = "{\n"
        + "    \"source\": \"Requirement\",\n"
        + "    \"target\": \"Design\",\n"
        + "    \"file\": \"Requirement2Design.csv\"\n"
        + "  }";

    @Test
    public void testSourceTypeNotFound() throws IOException, ServerError {
        String sourceTypeName = "requirement";
        String targetTypeName = "design";
        ProjectVersion projectVersion = createProjectUploadedResources("testName");
        Project project = projectVersion.getProject();
        JSONObject traceMatrixDefinition = new JSONObject(jsonString);

        // VP - verify that target type not found
        Exception sourceException = assertThrows(ServerError.class, () -> {
            traceFileParser.findMatrixArtifactTypes(project, traceMatrixDefinition);
        });
        assertThat(sourceException.getMessage()).as("source error message")
            .containsIgnoringCase("source").contains("not exist");

        // VP - verify that source type is found but not target
        ArtifactType sourceType = new ArtifactType(project, sourceTypeName);
        this.artifactTypeRepository.save(sourceType);
        Exception targetException = assertThrows(ServerError.class, () -> {
            traceFileParser.findMatrixArtifactTypes(project, traceMatrixDefinition);
        });
        assertThat(targetException.getMessage()).as("target error message")
            .containsIgnoringCase("target").contains("not exist");

        // VP - verify that source and target types found
        ArtifactType targetType = new ArtifactType(project, targetTypeName);
        this.artifactTypeRepository.save(targetType);
        Pair<ArtifactType, ArtifactType> artifactTypes = traceFileParser.findMatrixArtifactTypes(project,
            traceMatrixDefinition);
        assertThat(artifactTypes.getValue0().getName()).as("source type found").isEqualTo(sourceTypeName);
        assertThat(artifactTypes.getValue1().getName()).as("target type found").isEqualTo(targetTypeName);

        projectService.deleteProject(project);
    }
}
