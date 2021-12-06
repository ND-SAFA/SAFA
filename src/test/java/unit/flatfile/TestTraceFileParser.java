package unit.flatfile;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.io.IOException;

import edu.nd.crc.safa.importer.flatfiles.TraceFileParser;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.db.ArtifactType;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import org.javatuples.Pair;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import unit.ApplicationBaseTest;

/**
 * Provides a smoke test for testing the TraceFileParser is able to create trace links.
 */
public class TestTraceFileParser extends ApplicationBaseTest {

    private final String jsonString = "{\n"
        + "    \"source\": \"Requirement\",\n"
        + "    \"target\": \"Design\",\n"
        + "    \"file\": \"Requirement2Design.csv\"\n"
        + "  }";
    
    @Autowired
    TraceFileParser traceFileParser;

    @Test
    public void testSourceTypeNotFound() throws IOException, SafaError {
        String sourceTypeName = "requirement";
        String targetTypeName = "design";
        ProjectVersion projectVersion = createProjectAndUploadBeforeFiles("testProject");
        Project project = projectVersion.getProject();
        JSONObject traceMatrixDefinition = new JSONObject(jsonString);

        // VP - verify that source type not found
        Exception sourceException = assertThrows(SafaError.class, () -> {
            traceFileParser.findMatrixArtifactTypes(project, traceMatrixDefinition);
        });
        assertThat(sourceException.getMessage()).matches(".*unknown type.*Requirement.*[\\s\\S]");

        // VP - verify that source type is found but not target
        ArtifactType sourceType = new ArtifactType(project, sourceTypeName);
        this.artifactTypeRepository.save(sourceType);
        Exception targetException = assertThrows(SafaError.class, () -> {
            traceFileParser.findMatrixArtifactTypes(project, traceMatrixDefinition);
        });
        assertThat(targetException.getMessage()).matches(".*unknown type.*Design.*[\\s\\S]");

        // VP - verify that source and target types found
        ArtifactType targetType = new ArtifactType(project, targetTypeName);
        this.artifactTypeRepository.save(targetType);
        Pair<ArtifactType, ArtifactType> artifactTypes = traceFileParser.findMatrixArtifactTypes(project,
            traceMatrixDefinition);
        assertThat(artifactTypes.getValue0().getName()).as("source type found").isEqualTo(sourceTypeName);
        assertThat(artifactTypes.getValue1().getName()).as("target type found").isEqualTo(targetTypeName);
    }
}
