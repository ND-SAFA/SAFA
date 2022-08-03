package unit.jobs;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.server.entities.api.jira.JiraIssueDTO;
import edu.nd.crc.safa.server.entities.api.jobs.JobType;
import edu.nd.crc.safa.server.entities.app.JobSteps;
import edu.nd.crc.safa.server.entities.db.JiraAccessCredentials;
import edu.nd.crc.safa.server.entities.db.JobDbEntity;
import edu.nd.crc.safa.utilities.FileUtilities;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.BeforeEach;

/**
 * Sets up internal SAFA and JIRA authentication in order to skip
 * testing the API directly.
 */
public abstract class JiraBaseFlatFileTest extends JobBaseFlatFileTest {

    String jiraProjectName = "test-jira-project";
    int N_STEPS = 5;
    String cloudId = UUID.randomUUID().toString();
    Long jiraProjectId = (long) 1;

    @BeforeEach
    public void setJiraAuthorization() {
        setAuthorization(); // Required because getting currentDocument requires a user be logged in

        // Step - Create fake credentials
        JiraAccessCredentials credentials = new JiraAccessCredentials();
        credentials.setUser(currentUser);
        credentials.setCloudId(cloudId);
        serviceProvider.getJiraAccessCredentialsRepository().save(credentials);

        // Step - Override steps to skip authentication and project retrieval
        JobSteps.jiraProjectCreationSteps = new String[]{
            JobSteps.jiraProjectCreationSteps[2],
            JobSteps.jiraProjectCreationSteps[3]
        };
    }

    @NotNull
    protected List<JiraIssueDTO> readJiraIssues(String pathToFile) throws IOException {
        JSONObject testProjectJson = FileUtilities.readJSONFile(pathToFile);
        JSONArray issuesJson = testProjectJson.getJSONArray("issues");
        List<JiraIssueDTO> issues = new ArrayList<>();
        for (int i = 0; i < issuesJson.length(); i++) {
            JSONObject issueJson = issuesJson.getJSONObject(i);
            JiraIssueDTO issue = toClass(issueJson.toString(), JiraIssueDTO.class);
            issues.add(issue);
        }
        return issues;
    }

    public JobDbEntity verifyJIRAJobWasCompleted(UUID jobId) {
        return super.verifyJobWasCompleted(jobId, N_STEPS);
    }

    public JobDbEntity createJIRAJob() {
        return this.jobService.createNewJob(JobType.JIRA_PROJECT_CREATION, jiraProjectName);
    }
}
