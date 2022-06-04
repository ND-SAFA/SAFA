package unit.jobs;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.server.entities.api.jira.JiraIssueDTO;
import edu.nd.crc.safa.server.entities.api.jobs.JiraProjectCreationWorker;
import edu.nd.crc.safa.server.entities.api.jobs.JobType;
import edu.nd.crc.safa.server.entities.app.JobStatus;
import edu.nd.crc.safa.server.entities.app.JobSteps;
import edu.nd.crc.safa.server.entities.db.ArtifactVersion;
import edu.nd.crc.safa.server.entities.db.JiraAccessCredentials;
import edu.nd.crc.safa.server.entities.db.JobDbEntity;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.JobDbRepository;
import edu.nd.crc.safa.server.services.ServiceProvider;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import org.apache.commons.io.FileUtils;
import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.security.test.context.support.WithUserDetails;

public class TestJiraProjectCreation extends JobBaseTest {

    @Autowired
    JobDbRepository jobDbRepository;

    @Autowired
    ServiceProvider serviceProvider;

    @BeforeEach
    public void setAuthorization() {
        Claims claims = Jwts.claims().setSubject(currentUsername);
        UsernamePasswordAuthenticationToken authorization = new UsernamePasswordAuthenticationToken(claims,
            null,
            new ArrayList<>());
        SecurityContextHolder.getContext().setAuthentication(authorization);
    }

    @Test
    @WithMockUser(currentUsername)
    @WithUserDetails(currentUsername)
    public void testImportDroneResponse() throws Exception {
        // Step - Set constants
        String cloudId = "";
        Long jiraProjectId = (long) 1;

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

        // Step - Create job
        JobDbEntity jobDbEntity = this.jobService.createNewJob(JobType.JIRA_PROJECT_CREATION, "jira-test");

        // Step - Create worker
        JiraProjectCreationWorker job = new JiraProjectCreationWorker(
            jobDbEntity,
            serviceProvider,
            jiraProjectId,
            cloudId
        );

        // Step - Read test json file
        JSONObject testProjectJson = readFile(ProjectPaths.PATH_TO_DRONE_ISSUES);
        JSONArray issuesJson = testProjectJson.getJSONArray("issues");
        int nArtifacts = testProjectJson.getInt("maxResults");

        // Step - Map issues
        List<JiraIssueDTO> issues = new ArrayList<>();
        for (int i = 0; i < issuesJson.length(); i++) {
            JSONObject issueJson = issuesJson.getJSONObject(i);
            JiraIssueDTO issue = toClass(issueJson.toString(), JiraIssueDTO.class);
            issues.add(issue);
        }

        // VP - Verify issues were parsed
        job.setIssues(issues);
        assertThat(issues.size()).isEqualTo(nArtifacts);

        // Step - Run job
        serviceProvider.getJobService().runJobWorker(
            jobDbEntity,
            serviceProvider,
            job
        );

        // Step - Retrieve completed project
        jobDbEntity = jobService.getJobById(job.getJobDbEntity().getId());
        UUID versionId = jobDbEntity.getCompletedEntityId();
        ProjectVersion projectVersion = projectVersionRepository.findByVersionId(versionId);

        // VP - Verify that project created
        jobDbEntity = jobService.getJobById(jobDbEntity.getId());
        assertThat(jobDbEntity.getStatus()).isEqualTo(JobStatus.COMPLETED);
        assertThat(jobDbEntity.getCurrentProgress()).isEqualTo(100);

        // VP - Verify that artifacts were created
        List<ArtifactVersion> artifacts = this.artifactVersionRepository.findByProjectVersion(projectVersion);
        assertThat(artifacts.size()).isEqualTo(nArtifacts);
    }

    public JSONObject readFile(String path) throws IOException {
        String fileContent = FileUtils.readFileToString(new File(path), "utf-8");
        return new JSONObject(fileContent);
    }
}
