package unit.project.matrices;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.List;

import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.TraceMatrix;
import edu.nd.crc.safa.server.repositories.traces.TraceMatrixRepository;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

/**
 * Tests that projects defined in database are able to be retrieved by user.
 */
public class CreateTraceMatrix extends TraceMatrixBaseTest {

    @Autowired
    TraceMatrixRepository traceMatrixRepository;

    @Test
    public void createTraceMatrix() throws Exception {
        Project project = this.createEmptyProject();

        // VP - Assert that single matrix exists for project.
        List<TraceMatrix> projectMatrices = traceMatrixRepository.findByProject(project);
        assertThat(projectMatrices.size()).isEqualTo(0);

        // Step - Send request
        String route = RouteBuilder
            .withRoute(AppRoutes.Projects.TraceMatrix.createTraceMatrix)
            .withProject(project)
            .withSourceArtifactTypeName(sourceArtifactTypeName)
            .withTargetArtifactTypeName(targetArtifactTypeName)
            .buildEndpoint();
        sendPost(route, new JSONObject(), status().isOk());

        // VP - Assert that single matrix exists for project.
        projectMatrices = traceMatrixRepository.findByProject(project);
        assertThat(projectMatrices.size()).isEqualTo(1);
    }
}
