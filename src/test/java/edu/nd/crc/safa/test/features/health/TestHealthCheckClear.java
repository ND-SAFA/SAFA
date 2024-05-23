package edu.nd.crc.safa.test.features.health;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.comments.entities.dtos.ArtifactCommentResponseDTO;
import edu.nd.crc.safa.features.health.entities.HealthResponseDTO;
import edu.nd.crc.safa.features.health.entities.gen.GenHealthResponse;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.features.generation.GenerationalTest;

import org.junit.jupiter.api.Test;

class TestHealthCheckClear extends GenerationalTest {
    /**
     * Tests that health checks performed a second time will clear the initial health checks.
     */
    @Test
    void testHealthChecksClear() {
        ProjectVersion projectVersion = rootBuilder.actions(a -> a.createProjectWithVersion(getCurrentUser())).get();
        HealthCheckTestData testData = new HealthCheckTestData();

        UUID artifactId = testData.createProjectArtifacts(projectVersion, this.dbEntityBuilder);
        ArtifactAppEntity targetArtifact = new ArtifactAppEntity();
        targetArtifact.setId(artifactId);

        List<Artifact> projectArtifacts = getServiceProvider()
            .getArtifactRepository()
            .getProjectArtifacts(projectVersion.getProject().getId());
        HealthCheckTestVerifier testVerifier = new HealthCheckTestVerifier(projectVersion, projectArtifacts);

        // Step - Trigger health
        mockHealthResponse(testData.createMockGenHealthResponse());

        HealthResponseDTO healthResponseDTO = getServiceProvider()
            .getHealthService()
            .performArtifactHealthChecks(projectVersion, targetArtifact);


        testVerifier.verifyHealthResponse(healthResponseDTO);

        ArtifactCommentResponseDTO artifactComments =
            getServiceProvider().getCommentRetrievalService().getArtifactComments(artifactId);

        testVerifier.verifyArtifactComments(artifactComments);
    }

    public void mockHealthResponse(GenHealthResponse genResponse) {
        getServer().setJobResponse(genResponse);
    }
}
