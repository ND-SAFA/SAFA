package unit.project.matrices;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.builders.CommitBuilder;
import edu.nd.crc.safa.server.entities.db.ArtifactType;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.TraceMatrix;
import edu.nd.crc.safa.server.repositories.entities.TraceMatrixRepository;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

/**
 * Tests that projects defined in database are able to be retrieved by user.
 */
public class AttemptToCreateLoop extends TraceMatrixBaseTest {

    @Autowired
    TraceMatrixRepository traceMatrixRepository;

    @Test
    public void getTraceMatrices() throws Exception {
        String sourceArtifactName = "RE-10";
        String targetArtifactName = "DD-20";

        // Step - Create project, artifact types, and artifacts.
        Project project = this.createEmptyProject();
        ArtifactType sourceArtifactType = this.dbEntityBuilder.getType(projectName, sourceArtifactTypeName);
        ArtifactType targetArtifactType = this.dbEntityBuilder.getType(projectName, targetArtifactTypeName);

        // Step - Create trace matrix object manually
        TraceMatrix traceMatrix = new TraceMatrix(project, sourceArtifactType, targetArtifactType);
        this.traceMatrixRepository.save(traceMatrix);

        // Step - Create source and target artifacts
        dbEntityBuilder
            .newArtifact(projectName, sourceArtifactTypeName, sourceArtifactName)
            .newArtifact(projectName, targetArtifactTypeName, targetArtifactName);
        ProjectVersion projectVersion = dbEntityBuilder.getProjectVersion(projectName, 0);

        // Step - Create a trace link in the wrong direction: target -> source
        JSONObject traceJson = jsonBuilder
            .withProject(projectName, projectName, "")
            .withTraceAndReturn(projectName, targetArtifactName, sourceArtifactName);
        CommitBuilder commitBuilder = CommitBuilder.withVersion(projectVersion).withAddedTrace(traceJson);

        JSONObject responseBody = commitWithStatus(commitBuilder, status().is4xxClientError());
        String errorMessage = responseBody.getString("message");
        assertThat(errorMessage).matches(".*direction.*");
    }
}
