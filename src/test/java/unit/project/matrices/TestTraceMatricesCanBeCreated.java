package unit.project.matrices;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import edu.nd.crc.safa.builders.requests.SafaRequest;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactType;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.matrices.entities.TraceMatrix;
import edu.nd.crc.safa.features.traces.repositories.TraceMatrixRepository;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

/**
 * Tests that projects defined in database are able to be retrieved by user.
 */
class TestTraceMatricesCanBeCreated extends TraceMatrixBase {

    @Autowired
    TraceMatrixRepository traceMatrixRepository;

    @Test
    void testCreateDeleteRetrieveTraceMatrices() throws Exception {
        Project project = this.createEmptyProject();
        ArtifactType sourceArtifactType = this.dbEntityBuilder.getType(projectName, sourceArtifactTypeName);
        ArtifactType targetArtifactType = this.dbEntityBuilder.getType(projectName, targetArtifactTypeName);

        // Step - Create trace matrix object manually
        TraceMatrix traceMatrix = new TraceMatrix(project, sourceArtifactType, targetArtifactType);
        this.traceMatrixRepository.save(traceMatrix);

        // Step - Send request to retrieve matrix.
        JSONObject projectMatrices = new SafaRequest(AppRoutes.Projects.TraceMatrix.GET_TRACE_MATRICES)
            .withProject(project)
            .getWithJsonObject();

        // VP - Assert that no matrix exists for project.
        assertThat(projectMatrices.has(sourceArtifactTypeName)).isTrue();
        JSONArray targetArtifactTypes = projectMatrices.getJSONArray(sourceArtifactTypeName);
        assertThat(targetArtifactTypes.get(0)).isEqualTo(targetArtifactTypeName);
    }
}
