package features.matrices.crud;

import static org.assertj.core.api.Assertions.assertThat;

import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.builders.requests.SafaRequest;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactType;
import edu.nd.crc.safa.features.matrices.entities.TraceMatrix;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.traces.repositories.TraceMatrixRepository;

import features.matrices.base.AbstractMatrixTest;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

/**
 * Tests that client is able to delete a trace matrix.
 */
class TestDeleteTraceMatrix extends AbstractMatrixTest {

    @Autowired
    TraceMatrixRepository traceMatrixRepository;

    @Test
    void testDeleteTraceMatrix() throws Exception {
        Project project = this.createEmptyProject();
        ArtifactType sourceArtifactType = this.dbEntityBuilder.getType(projectName, sourceArtifactTypeName);
        ArtifactType targetArtifactType = this.dbEntityBuilder.getType(projectName, targetArtifactTypeName);

        // Step - Create trace matrix object manually
        TraceMatrix traceMatrix = new TraceMatrix(project, sourceArtifactType, targetArtifactType);
        this.traceMatrixRepository.save(traceMatrix);

        // Step - Send request to delete matrix.
        String route = RouteBuilder
            .withRoute(AppRoutes.TraceMatrix.DELETE_TRACE_MATRIX)
            .withProject(project)
            .withSourceArtifactTypeName(sourceArtifactTypeName)
            .withTargetArtifactTypeName(targetArtifactTypeName)
            .buildEndpoint();
        SafaRequest.withRoute(route).deleteWithJsonObject();

        // VP - Assert that no matrix exists for project.
        int nMatrices = traceMatrixRepository.findByProject(project).size();
        assertThat(nMatrices).isZero();
    }
}
