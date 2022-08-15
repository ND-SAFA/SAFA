package features.matrices.crud;


import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;

import edu.nd.crc.safa.builders.requests.SafaRequest;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.matrices.entities.TraceMatrix;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.traces.repositories.TraceMatrixRepository;

import features.matrices.base.AbstractMatrixTest;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

/**
 * Tests that projects defined in database are able to be retrieved by user.
 */
class TestCreateTraceMatrix extends AbstractMatrixTest {

    @Autowired
    TraceMatrixRepository traceMatrixRepository;

    @Test
    void createTraceMatrix() throws Exception {
        Project project = this.createEmptyProject();

        // VP - Assert that single matrix exists for project.
        List<TraceMatrix> projectMatrices = traceMatrixRepository.findByProject(project);
        assertThat(projectMatrices).isEmpty();

        // Step - Send request
        SafaRequest
            .withRoute(AppRoutes.TraceMatrix.CREATE_TRACE_MATRIX)
            .withProject(project)
            .withSourceArtifactTypeName(sourceArtifactTypeName)
            .withTargetArtifactTypeName(targetArtifactTypeName)
            .postWithJsonObject(new JSONObject());

        // VP - Assert that single matrix exists for project.
        projectMatrices = traceMatrixRepository.findByProject(project);
        assertThat(projectMatrices.size()).isEqualTo(1);
    }
}
