package features.jobs.logic.json;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.HashMap;
import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.builders.requests.SafaRequest;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;
import edu.nd.crc.safa.utilities.JsonFileUtilities;

import features.base.ApplicationBaseTest;
import features.jobs.base.JobTestService;
import org.junit.jupiter.api.Test;

/**
 * Responsible for testing that a project can be created via JSON
 * by submitting a job
 */
class TestJsonProjectCreationJob extends ApplicationBaseTest {
    final String description = "description";
    final int N_STEPS = 1;
    final ArtifactAppEntity artifactAppEntity = new ArtifactAppEntity(
        "",
        ArtifactConstants.type,
        ArtifactConstants.name,
        ArtifactConstants.summary,
        ArtifactConstants.body,
        ArtifactConstants.documentType,
        new HashMap<>()
    );

    @Test
    void testCreateProjectViaJson() throws Exception {
        // Step 1 - Create project
        ProjectAppEntity projectAppEntity = new ProjectAppEntity();
        projectAppEntity.setName(projectName);
        projectAppEntity.setDescription(description);
        projectAppEntity.setArtifacts(List.of(artifactAppEntity));

        // Step 2 - Submit project to be created
        String jobIdString = SafaRequest
            .withRoute(AppRoutes.Jobs.JSON_PROJECT_JOB)
            .postWithJsonObject(JsonFileUtilities.toJson(projectAppEntity))
            .getString("id");
        UUID jobId = UUID.fromString(jobIdString);

        // Step - Get Job and subscribe for updates
        createNewConnection(defaultUser).subscribeToJob(defaultUser, jobService.getJobById(jobId));

        // VP - Verify that job has finished.
        JobTestService.verifyJobWasCompleted(serviceProvider, jobId, N_STEPS);

        // VP - Verify that all entities were created
        UUID versionId = serviceProvider.getJobService().getJobById(jobId).getCompletedEntityId();

        // Step - Retrieve project created
        ProjectVersion projectVersion = this.projectVersionRepository.findByVersionId(versionId);
        ProjectAppEntity project = getProjectAtVersion(projectVersion);

        // VP - Verify project was created with name and description
        assertThat(project.getName()).isEqualTo(projectName);
        assertThat(project.getDescription()).isEqualTo(description);

        // VP - Verify artifact was created
        ArtifactAppEntity artifact = project.artifacts.get(0);
        assertThat(artifact.name).isEqualTo(ArtifactConstants.name);
        assertThat(artifact.type).isEqualTo(ArtifactConstants.type);
        assertThat(artifact.summary).isEqualTo(ArtifactConstants.summary);
        assertThat(artifact.body).isEqualTo(ArtifactConstants.body);
        assertThat(artifact.getDocumentType()).isEqualTo(ArtifactConstants.documentType);
    }

    static class ArtifactConstants {
        static String name = "name";
        static String type = "type";
        static String body = "body";
        static String summary = "summary";
        static DocumentType documentType = DocumentType.ARTIFACT_TREE;
    }
}
