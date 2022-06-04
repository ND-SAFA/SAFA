package unit.jobs;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.server.entities.api.jira.JiraIssueDTO;
import edu.nd.crc.safa.server.entities.api.jobs.JiraProjectCreationWorker;
import edu.nd.crc.safa.server.entities.db.JobDbEntity;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import org.junit.jupiter.api.Test;
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.security.test.context.support.WithUserDetails;

public class TestJiraProjectCreation extends JiraBaseTest {

    @Test
    @WithMockUser(currentUsername)
    @WithUserDetails(currentUsername)
    public void testImportDroneResponse() throws Exception {
        // Step - Create job
        JobDbEntity jobDbEntity = createJIRAJob();

        // Step - Read test json file
        List<JiraIssueDTO> issues = readJiraIssues(ProjectPaths.PATH_TO_DRONE_ISSUES);
        int nArtifacts = issues.size();

        // Step - Create job and worker
        JiraProjectCreationWorker job = new JiraProjectCreationWorker(
            jobDbEntity,
            serviceProvider,
            jiraProjectId,
            cloudId
        );
        job.setIssues(issues);

        // Step - Run job
        serviceProvider
            .getJobService()
            .runJobWorker(jobDbEntity, serviceProvider, job);

        // VP - Verify that project completed
        JobDbEntity completedJob = verifyJIRAJobWasCompleted(jobDbEntity.getId());

        // VP - Verify that artifacts were created
        UUID versionId = completedJob.getCompletedEntityId();
        ProjectVersion projectVersion = projectVersionRepository.findByVersionId(versionId);
        verifyNumberOfItems("artifacts",
            () -> this.artifactVersionRepository.findByProjectVersion(projectVersion),
            nArtifacts);
    }
}
