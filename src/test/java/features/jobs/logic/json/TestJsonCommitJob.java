package features.jobs.logic.json;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.utilities.JsonFileUtilities;

import common.EntityConstants;
import features.base.ApplicationBaseTest;
import features.jobs.base.JobTestService;
import org.junit.jupiter.api.Test;
import requests.SafaRequest;

/**
 * Responsible for testing that a project can be created via JSON
 * by submitting a job
 */
class TestJsonCommitJob extends ApplicationBaseTest {
    final String description = "description";
    final int N_STEPS = 1;
    EntityConstants.ArtifactConstants artifactConstants = new EntityConstants.ArtifactConstants();

    @Test
    void testCreateProjectViaJson() throws Exception {
        // Step 1 - Create project
        ProjectAppEntity projectAppEntity = new ProjectAppEntity();
        projectAppEntity.setName(projectName);
        projectAppEntity.setDescription(description);
        projectAppEntity.setArtifacts(List.of(artifactConstants.artifact));

        // Step 2 - Submit project to be created
        String jobIdString = SafaRequest
            .withRoute(AppRoutes.Jobs.CREATE_PROJECT_VIA_JSON)
            .postWithJsonObject(JsonFileUtilities.toJson(projectAppEntity))
            .getString("id");
        UUID jobId = UUID.fromString(jobIdString);

        // Step - Get Job and subscribe for updates
        notificationService.createNewConnection(defaultUser).subscribeToJob(defaultUser,
            jobService.getJobById(jobId));

        // VP - Verify that job has finished.
        JobTestService.verifyJobWasCompleted(serviceProvider, jobId, N_STEPS);

        // VP - Verify that all entities were created
        UUID versionId = serviceProvider.getJobService().getJobById(jobId).getCompletedEntityId();

        // Step - Retrieve project created
        ProjectVersion projectVersion = this.projectVersionRepository.findByVersionId(versionId);
        ProjectAppEntity project = retrievalService.getProjectAtVersion(projectVersion);

        // VP - Verify project was created with name and description
        assertThat(project.getName()).isEqualTo(projectName);
        assertThat(project.getDescription()).isEqualTo(description);

        // VP - Verify artifact was created
        ArtifactAppEntity artifact = project.getArtifacts().get(0);
        assertThat(artifact.name).isEqualTo(artifactConstants.name);
        assertThat(artifact.type).isEqualTo(artifactConstants.type);
        assertThat(artifact.summary).isEqualTo(artifactConstants.summary);
        assertThat(artifact.body).isEqualTo(artifactConstants.body);
        assertThat(artifact.getDocumentType()).isEqualTo(artifactConstants.documentType);
    }
}
