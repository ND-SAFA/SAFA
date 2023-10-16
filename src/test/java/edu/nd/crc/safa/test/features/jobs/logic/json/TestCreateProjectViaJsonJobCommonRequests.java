package edu.nd.crc.safa.test.features.jobs.logic.json;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.jobs.entities.app.CreateProjectByJsonPayload;
import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.common.EntityConstants;
import edu.nd.crc.safa.test.features.jobs.base.JobTestService;
import edu.nd.crc.safa.test.requests.SafaRequest;
import edu.nd.crc.safa.test.services.requests.CommonProjectRequests;

import org.junit.jupiter.api.Test;

/**
 * Responsible for testing that a project can be created via JSON
 * by submitting a job
 */
class TestCreateProjectViaJsonJobCommonRequests extends ApplicationBaseTest {
    final String description = "description";
    final int N_STEPS = 4;
    EntityConstants.ArtifactConstants artifactConstants = new EntityConstants.ArtifactConstants();

    @Test
    void testCreateProjectViaJson() throws Exception {
        // Step 1 - Create project
        ProjectAppEntity projectAppEntity = new ProjectAppEntity();
        projectAppEntity.setName(projectName);
        projectAppEntity.setDescription(description);
        projectAppEntity.setArtifacts(List.of(artifactConstants.artifact));

        // Step 2 - Submit project to be created
        CreateProjectByJsonPayload payload = new CreateProjectByJsonPayload();
        payload.setProject(projectAppEntity);
        String jobIdString = SafaRequest
            .withRoute(AppRoutes.Jobs.Projects.CREATE_PROJECT_VIA_JSON)
            .postWithJsonObject(payload)
            .getString("id");
        UUID jobId = UUID.fromString(jobIdString);

        // Step - Get Job and subscribe for updates
        this.rootBuilder
            .notifications(n -> n
                .initializeUser(getCurrentUser(), getToken(getCurrentUser())).subscribeToJob(getCurrentUser(), jobService.getJobById(jobId)));
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
        assertThat(artifact.getName()).isEqualTo(artifactConstants.name);
        assertThat(artifact.getType()).isEqualTo(artifactConstants.type);
        assertThat(artifact.getSummary()).isEqualTo(artifactConstants.summary);
        assertThat(artifact.getBody()).isEqualTo(artifactConstants.body);

        // VP - Verify that job is associated with project
        List<JobAppEntity> projectJobs = CommonProjectRequests.getProjectJobs(projectVersion.getProject());
        assertThat(projectJobs).hasSize(1);
    }
}
