package features.jobs.logic.jira;

import java.util.List;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.jira.entities.api.JiraIdentifier;
import edu.nd.crc.safa.features.jira.entities.app.JiraIssueDTO;
import edu.nd.crc.safa.features.jira.entities.app.JiraProjectResponseDTO;
import edu.nd.crc.safa.features.jobs.entities.app.JiraProjectCreationJob;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
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
        List<JiraIssueDTO> issues = readJiraIssues(ProjectPaths.Tests.Jira.DRONE_ISSUES);
        /**
         * Now counts inward + outward issues not accounted for
         * Note, this includes an extra one because it is referenced there.
         * This artifact definitely exists but was just under the cutoff for
         */
        int nArtifacts = issues.size() + 1;

        // Step - Create skeleton project
        Project project = new Project("", ""); // Set once parse starts
        this.serviceProvider.getProjectService().saveProjectWithCurrentUserAsOwner(project);
        ProjectVersion projectVersion = this.serviceProvider.getProjectService().createInitialProjectVersion(project);
        JiraIdentifier jiraIdentifier = new JiraIdentifier(projectVersion, jiraProjectId, cloudId);

        // Step - Create job and worker
        JiraProjectCreationJob job = new JiraProjectCreationJob(
            jobDbEntity,
            serviceProvider,
            jiraIdentifier
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
