package edu.nd.crc.safa.test.features.jobs.logic.jira;

import java.util.List;
import java.util.stream.IntStream;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.jira.entities.api.JiraIdentifier;
import edu.nd.crc.safa.features.jira.entities.api.JiraImportSettings;
import edu.nd.crc.safa.features.jira.entities.app.JiraIssueDTO;
import edu.nd.crc.safa.features.jira.entities.app.JiraProjectResponseDTO;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.jobs.entities.jobs.JiraProjectImportJob;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.features.jobs.base.JiraBaseFlatFileTest;

import org.junit.jupiter.api.Test;

/**
 * Test importing a JIRA project into an existing SAFA projects
 */
class TestFlatFileJiraProjectImportCommonRequests extends JiraBaseFlatFileTest {

    /**
     * Tests that the sample DroneResponse JSON file is able
     * to be parsed and project created.
     *
     * @throws Exception Throws exception is error encountered while reading JSON file.
     */
    @Test
    void testImportDroneResponseIntoExisting() throws Exception {
        // Step - Create job
        JobDbEntity jobDbEntity = createJIRAJob();

        // Step - Read test json file
        List<JiraIssueDTO> issues = readJiraIssues(ProjectPaths.Resources.Tests.Jira.DRONE_ISSUES);
        /*
         * Now counts inward + outward issues not accounted for
         * Note, this includes an extra one because it is referenced there.
         * This artifact definitely exists but was just under the cutoff for
         */
        int initialArtifactCount = 5;
        int nArtifacts = issues.size() + 1;

        this.createBaseSafaProject(projectName, initialArtifactCount);

        ProjectVersion projectVersion = dbEntityBuilder.getProjectVersion(projectName, 0);
        Project project = dbEntityBuilder.getProject(projectName);
        JiraIdentifier jiraIdentifier = new JiraIdentifier(projectVersion, jiraProjectId, orgId);

        // Step - Create job and worker
        JiraProjectImportJob job = new JiraProjectImportJob(
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
        verifyJIRAJobWasCompleted(jobDbEntity.getId());

        // VP - Verify that artifacts were created
        verifyNumberOfItems("artifacts",
            () -> this.artifactRepository.findByProjectId(project.getId()),
            nArtifacts + initialArtifactCount);
    }

    private JiraProjectResponseDTO createMockJiraProject() {
        JiraProjectResponseDTO mockJiraResponse = new JiraProjectResponseDTO();

        mockJiraResponse.setName("Mock Project Name");
        mockJiraResponse.setDescription("sample project description");
        return mockJiraResponse;
    }

    protected void createBaseSafaProject(String projectName, int initialArtifactCount) {
        String artifactTypeName = "requirement";

        dbEntityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .newType(projectName, artifactTypeName);

        IntStream.range(0, initialArtifactCount).mapToObj(String::valueOf)
                .forEach(name -> dbEntityBuilder.newArtifact(projectName, artifactTypeName, name));
    }
}
