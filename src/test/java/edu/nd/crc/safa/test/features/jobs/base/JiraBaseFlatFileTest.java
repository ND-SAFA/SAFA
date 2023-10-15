package edu.nd.crc.safa.test.features.jobs.base;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.authentication.AuthorizationSetter;
import edu.nd.crc.safa.features.jira.entities.app.JiraIssueDTO;
import edu.nd.crc.safa.features.jira.entities.db.JiraAccessCredentials;
import edu.nd.crc.safa.features.jobs.entities.app.JobSteps;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.jobs.entities.jobs.CreateProjectViaJiraJob;
import edu.nd.crc.safa.test.features.flatfiles.base.BaseFlatFileTest;
import edu.nd.crc.safa.test.services.MappingTestService;
import edu.nd.crc.safa.utilities.JsonFileUtilities;

import jakarta.validation.constraints.NotNull;
import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;

/**
 * Sets up internal SAFA and JIRA authentication in order to skip
 * testing the API directly.
 */
public abstract class JiraBaseFlatFileTest extends BaseFlatFileTest {

    protected String jiraProjectName = "test-jira-project";
    protected int N_STEPS = 7;
    protected UUID orgId = UUID.randomUUID();
    protected Long jiraProjectId = (long) 1;
    protected String[] originalJraProjectCreationSteps;

    @BeforeEach
    public void setJiraAuthorization() {
        AuthorizationSetter.setSessionAuthorization(currentUserName, serviceProvider);

        // Step - Create fake credentials
        JiraAccessCredentials credentials = new JiraAccessCredentials();
        credentials.setUser(getCurrentUser());
        serviceProvider.getJiraAccessCredentialsRepository().save(credentials);

        originalJraProjectCreationSteps = Arrays.stream(JobSteps.jiraProjectCreationSteps).toArray(String[]::new);
        // Step - Override steps to skip authentication and project retrieval
        JobSteps.jiraProjectCreationSteps = new String[]{
            JobSteps.jiraProjectCreationSteps[2],
            JobSteps.jiraProjectCreationSteps[3]
        };
    }

    @AfterEach
    public void restoreSteps() {
        JobSteps.jiraProjectCreationSteps = originalJraProjectCreationSteps;
    }

    @NotNull
    protected List<JiraIssueDTO> readJiraIssues(String pathToFile) throws IOException {
        JSONObject testProjectJson = JsonFileUtilities.readJSONFile(pathToFile);
        JSONArray issuesJson = testProjectJson.getJSONArray("issues");
        List<JiraIssueDTO> issues = new ArrayList<>();
        for (int i = 0; i < issuesJson.length(); i++) {
            JSONObject issueJson = issuesJson.getJSONObject(i);
            JiraIssueDTO issue = MappingTestService.toClass(issueJson.toString(), JiraIssueDTO.class);
            issues.add(issue);
        }
        return issues;
    }

    public JobDbEntity verifyJIRAJobWasCompleted(UUID jobId) {
        return JobTestService.verifyJobWasCompleted(serviceProvider, jobId, N_STEPS);
    }

    public JobDbEntity createJIRAJob() {
        return this.jobService.createNewJob(CreateProjectViaJiraJob.class, jiraProjectName);
    }
}
