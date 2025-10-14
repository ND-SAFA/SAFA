package edu.nd.crc.safa.test.features.health;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.comments.entities.dtos.ArtifactCommentResponseDTO;
import edu.nd.crc.safa.features.health.entities.HealthRequest;
import edu.nd.crc.safa.features.health.entities.HealthResponseDTO;
import edu.nd.crc.safa.features.health.entities.HealthTask;
import edu.nd.crc.safa.features.health.entities.gen.GenHealthResponse;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.features.generation.GenerationalTest;

import org.junit.jupiter.api.Test;

class TestHealthChecks extends GenerationalTest {


    @Test
    void testHealthChecks() {
        ProjectVersion projectVersion = rootBuilder.actions(a -> a.createProjectWithVersion(getCurrentUser())).get();
        HealthCheckTestData testData = new HealthCheckTestData();

        UUID artifactId = testData.createProjectArtifacts(projectVersion, this.dbEntityBuilder);
        ArtifactAppEntity targetArtifact = new ArtifactAppEntity();
        targetArtifact.setId(artifactId);

        List<Artifact> projectArtifacts =
            getServiceProvider().getArtifactRepository().getProjectArtifacts(projectVersion.getProject().getId());

        GenHealthResponse mockResponse = testData.createMockGenHealthResponse();
        mockHealthResponse(mockResponse);

        HealthRequest request = new HealthRequest();
        request.setArtifactIds(List.of(targetArtifact.getId()));
        request.setTasks(List.of(HealthTask.CONTRADICTION, HealthTask.CONCEPT_EXTRACTION, HealthTask.CONCEPT_MATCHING));

        HealthResponseDTO healthResponseDTO = getServiceProvider()
            .getHealthService()
            .performHealthChecks(
                getCurrentUser(),
                projectVersion,
                request);

        HealthCheckTestVerifier testVerifier = new HealthCheckTestVerifier(projectVersion, projectArtifacts);
        testVerifier.verifyHealthResponse(healthResponseDTO);

        ArtifactCommentResponseDTO artifactComments =
            getServiceProvider().getCommentRetrievalService().getArtifactComments(artifactId);

        testVerifier.verifyArtifactComments(artifactComments);
    }

    public void mockHealthResponse(GenHealthResponse genResponse) {
        getServer().setJobResponse(genResponse);
    }
}
