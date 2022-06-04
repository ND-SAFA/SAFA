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

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.BeforeEach;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;

/**
 * Sets up internal SAFA and JIRA authentication in order to skip
 * testing the API directly.
 */
public class JiraBaseTest extends JobBaseTest {

    String jiraProjectName = "test-jira-project";
    int N_STEPS = 5;
    String cloudId = UUID.randomUUID().toString();
    Long jiraProjectId = (long) 1;

    @BeforeEach
    public void setAuthorization() {
        Claims claims = Jwts.claims().setSubject(currentUsername);
        UsernamePasswordAuthenticationToken authorization = new UsernamePasswordAuthenticationToken(claims,
            null,
            new ArrayList<>());
        SecurityContextHolder.getContext().setAuthentication(authorization);

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
