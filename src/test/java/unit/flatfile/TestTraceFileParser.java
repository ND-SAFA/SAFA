package unit.flatfile;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.io.IOException;

import edu.nd.crc.safa.server.db.entities.sql.Artifact;
import edu.nd.crc.safa.server.db.entities.sql.ArtifactType;
import edu.nd.crc.safa.server.db.entities.sql.Project;
import edu.nd.crc.safa.server.db.entities.sql.ProjectVersion;
import edu.nd.crc.safa.server.db.entities.sql.TraceLink;
import edu.nd.crc.safa.importer.flatfiles.TraceFileParser;
import edu.nd.crc.safa.server.responses.ServerError;

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

    @Test
    public void testCreateTestLinkMissingIds() throws IOException, ServerError {
        String sourceName = "RE-8";
        String targetName = "D-8";
        ProjectVersion projectVersion = createProjectUploadedResources("testName");
        Project project = projectVersion.getProject();

        ArtifactType sourceType = new ArtifactType(project, "requirement");
        ArtifactType targetType = new ArtifactType(project, "design");
        this.artifactTypeRepository.save(sourceType);
        this.artifactTypeRepository.save(targetType);

        Pair<ArtifactType, ArtifactType> artifactTypes = new Pair<>(sourceType, targetType);
        Pair<String, String> artifactIds = new Pair<>(sourceName, targetName);
        Exception sourceException = assertThrows(ServerError.class, () -> {
            traceFileParser.createTraceLink(project, artifactTypes, artifactIds);
        });
        assertThat(sourceException.getMessage()).as("source error message")
            .containsIgnoringCase("source").contains("not exist");

        // VP - source is found but not target artifact
        Artifact sourceArtifact = new Artifact(project, sourceType, sourceName);
        this.artifactRepository.save(sourceArtifact);
        Exception targetException = assertThrows(ServerError.class, () -> {
            traceFileParser.createTraceLink(project, artifactTypes, artifactIds);
        });
        assertThat(targetException.getMessage()).as("target error message")
            .containsIgnoringCase("target").contains("not exist");

        // VP - both source and target artifacts are found
        Artifact targetArtifact = new Artifact(project, targetType, targetName);
        this.artifactRepository.save(targetArtifact);
        TraceLink newLink = traceFileParser.createTraceLink(project, artifactTypes, artifactIds);
        assertThat(newLink).as("trace links created").isNotNull();

        projectService.deleteProject(project);
    }
}
