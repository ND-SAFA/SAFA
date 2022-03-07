package unit.project.matrices;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import edu.nd.crc.safa.builders.RouteBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.db.ArtifactType;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.TraceMatrix;
import edu.nd.crc.safa.server.repositories.traces.TraceMatrixRepository;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;

/**
 * Tests that projects defined in database are able to be retrieved by user.
 */
public class GetTraceMatrices extends TraceMatrixBaseTest {

    @Autowired
    TraceMatrixRepository traceMatrixRepository;

    @Test
    public void getTraceMatrices() throws Exception {
        Project project = this.createEmptyProject();
        ArtifactType sourceArtifactType = this.dbEntityBuilder.getType(projectName, sourceArtifactTypeName);
        ArtifactType targetArtifactType = this.dbEntityBuilder.getType(projectName, targetArtifactTypeName);

        // Step - Create trace matrix object manually
        TraceMatrix traceMatrix = new TraceMatrix(project, sourceArtifactType, targetArtifactType);
        this.traceMatrixRepository.save(traceMatrix);

        // Step - Send request to delete matrix.
        String route = RouteBuilder
            .withRoute(AppRoutes.Projects.getTraceMatrices)
            .withProject(project)
            .get();
        JSONObject projectMatrices = sendGet(route, status().isOk());

        // VP - Assert that no matrix exists for project.
        assertThat(projectMatrices.has(sourceArtifactTypeName)).isTrue();
        JSONArray targetArtifactTypes = projectMatrices.getJSONArray(sourceArtifactTypeName);
        assertThat(targetArtifactTypes.get(0)).isEqualTo(targetArtifactTypeName);
    }
}
