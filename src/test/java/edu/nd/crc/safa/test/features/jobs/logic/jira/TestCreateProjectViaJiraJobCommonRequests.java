package edu.nd.crc.safa.test.features.jobs.logic.jira;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.jira.entities.api.JiraIdentifier;
import edu.nd.crc.safa.features.jira.entities.api.JiraImportSettings;
import edu.nd.crc.safa.features.jira.entities.app.JiraIssueDTO;
import edu.nd.crc.safa.features.jira.entities.app.JiraProjectResponseDTO;
import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.jobs.entities.jobs.CreateProjectViaJiraJob;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.features.jobs.base.JiraBaseFlatFileTest;
import edu.nd.crc.safa.test.services.requests.CommonProjectRequests;

import org.junit.jupiter.api.Test;

/**
 * Tests that JIRA issues and links can be parsed from JSON
 * and created in the form of artifacts and trace links.
 */
class TestCreateProjectViaJiraJobCommonRequests extends JiraBaseFlatFileTest {

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
        List<JiraIssueDTO> issues = readJiraIssues(ProjectPaths.Resources.Tests.Jira.DRONE_ISSUES);

        /*
         * Now counts inward + outward issues not accounted for
         * Note, this includes an extra one because it is referenced there.
         * This artifact definitely exists but was just under the cutoff for
         */
        int nArtifacts = issues.size() + 1;

        // Step - Create skeleton project
        JiraIdentifier jiraIdentifier = new JiraIdentifier(null, jiraProjectId, orgId);

        // Step - Create job and worker
        CreateProjectViaJiraJob job = new CreateProjectViaJiraJob(
            jobDbEntity,
            serviceProvider,
            jiraIdentifier,
            getCurrentUser(),
            new JiraImportSettings()
        );

        job.setJiraProjectResponse(createMockJiraProject());
        job.setIssues(issues);

        // Step - Run job
        job.getSkipSteps().addAll(List.of(1, 2));
        serviceProvider
            .getJobService()
            .executeJob(serviceProvider, job);

        // VP - Verify that project completed
        JobDbEntity completedJob = verifyJIRAJobWasCompleted(jobDbEntity.getId());
        UUID projectVersionId = completedJob.getCompletedEntityId();
        ProjectVersion projectVersion = serviceProvider.getProjectVersionRepository().findByVersionId(projectVersionId);

        // VP - Verify that artifacts were created
        verifyNumberOfItems("artifacts",
            () -> this.artifactVersionRepository.findByProjectVersion(projectVersion),
            nArtifacts);

        // VP - Verify that job is associated with project
        List<JobAppEntity> projectJobs = CommonProjectRequests.getProjectJobs(projectVersion.getProject());
        assertEquals(1, projectJobs.size());
    }

    private JiraProjectResponseDTO createMockJiraProject() {
        JiraProjectResponseDTO mockJiraResponse = new JiraProjectResponseDTO();

        mockJiraResponse.setName("Mock Project Name");
        mockJiraResponse.setDescription("sample project description");
        return mockJiraResponse;
    }
}
