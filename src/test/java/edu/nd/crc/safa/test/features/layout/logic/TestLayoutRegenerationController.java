package edu.nd.crc.safa.test.features.layout.logic;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.layout.entities.api.LayoutGenerationRequestDTO;
import edu.nd.crc.safa.features.layout.entities.db.ArtifactPosition;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.javatuples.Pair;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;

/**
 * Test each endoint of the layout regeneration controller.
 */
class TestLayoutRegenerationController extends ApplicationBaseTest {

    /**
     * Test that regenerating a documents layout will re-save all artifact positions.
     */
    @Test
    void testRegeneration() throws Exception {
        Pair<ProjectVersion, ProjectVersion> dualVersions = creationService.createDualVersions(projectName);
        ProjectVersion v1 = dualVersions.getValue0();
        ProjectVersion v2 = dualVersions.getValue1();
        Project project = v1.getProject();

        // VP - Verify V1 layout
        ProjectAppEntity project1 = retrievalService.getProjectAtVersion(v1);
        layoutTestService.verifyProjectLayout(project1);

        // VP - Verify V2 layout
        ProjectAppEntity project2 = retrievalService.getProjectAtVersion(v2);
        layoutTestService.verifyProjectLayout(project2);

        // Step - Delete layout positions
        this.serviceProvider.getArtifactPositionRepository().deleteAll();

        // VP - Verify that layout is empty
        ProjectAppEntity project3 = retrievalService.getProjectAtVersion(v1);
        assertThat(project3.getLayout()).isEmpty();

        // Step - Send regeneration request
        LayoutGenerationRequestDTO generationRequest = new LayoutGenerationRequestDTO();
        generationRequest.setDefaultDocument(true);
        JSONObject response = SafaRequest
            .withRoute(AppRoutes.Layout.REGENERATE_LAYOUT)
            .withVersion(v2)
            .postWithJsonObject(generationRequest);
        JSONObject defaultDocumentLayout = response.getJSONObject("defaultDocumentLayout");

        // VP - Verify that layout received contains valid position for each artifact.
        for (ArtifactAppEntity artifact : project2.getArtifacts()) {
            JSONObject artifactPosition = defaultDocumentLayout.getJSONObject(artifact.getId().toString());
            assertThat(artifactPosition.getDouble("x")).isPositive();
            assertThat(artifactPosition.getDouble("y")).isPositive();
        }

        // VP - Verify that a position was persisted for each artifact
        List<ArtifactPosition> defaultDocumentArtifactPositions =
            this.serviceProvider.getArtifactPositionRepository().findByProjectVersionProjectAndDocumentDocumentId(
                project,
                null);
        assertThat(defaultDocumentArtifactPositions).hasSize(project2.getArtifacts().size());
    }
}
