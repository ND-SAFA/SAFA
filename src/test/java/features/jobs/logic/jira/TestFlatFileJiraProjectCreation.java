package features.jobs.logic.jira;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.jira.entities.app.JiraIssueDTO;
import edu.nd.crc.safa.features.jira.entities.app.JiraProjectResponseDTO;
import edu.nd.crc.safa.features.jobs.entities.app.JiraProjectCreationJob;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

import features.jobs.base.JiraBaseFlatFileTest;
import org.junit.jupiter.api.Test;

/**
 * Tests that JIRA issues and links can be parsed from JSON
 * and created in the form of artifacts and trace links.
 */
class TestFlatFileJiraProjectCreation extends JiraBaseFlatFileTest {

    /**
     * Tests that the sample DroneResponse JSON file is able
     * to be parsed and project created.
     *
     * @throws Exception Throws exception is error encountered while reading JSON file.
     */
    @Test
    void testImportDroneResponse() throws Exception {
        // Step - Create job
        JobDbEntity jobDbEntity = createJIRAJob();

        // Step - Read test json file
        List<JiraIssueDTO> issues = readJiraIssues(ProjectPaths.PATH_TO_DRONE_ISSUES);
        int nArtifacts = issues.size();

        // Step - Create job and worker
        JiraProjectCreationJob job = new JiraProjectCreationJob(
            jobDbEntity,
            serviceProvider,
            jiraProjectId,
            cloudId
        );

        job.setJiraProjectResponse(createMockJiraProject());
        job.setIssues(issues);

        // Step - Run job
        serviceProvider
            .getJobService()
            .executeJob(jobDbEntity, serviceProvider, job);

        // VP - Verify that project completed
        JobDbEntity completedJob = verifyJIRAJobWasCompleted(jobDbEntity.getId());

        // VP - Verify that artifacts were created
        UUID versionId = completedJob.getCompletedEntityId();
        ProjectVersion projectVersion = projectVersionRepository.findByVersionId(versionId);
        verifyNumberOfItems("artifacts",
            () -> this.artifactVersionRepository.findByProjectVersion(projectVersion),
            nArtifacts);
    }

    private JiraProjectResponseDTO createMockJiraProject() {
        JiraProjectResponseDTO mockJiraResponse = new JiraProjectResponseDTO();

        mockJiraResponse.setName("Mock Project Name");
        mockJiraResponse.setDescription("sample project description");
        return mockJiraResponse;
    }
}
