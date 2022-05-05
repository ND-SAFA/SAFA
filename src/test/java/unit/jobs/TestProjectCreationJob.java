package unit.jobs;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.api.ProjectCommit;
import edu.nd.crc.safa.server.entities.app.JobStatus;
import edu.nd.crc.safa.server.entities.db.Job;
import edu.nd.crc.safa.server.repositories.JobRepository;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import unit.ApplicationBaseTest;

public class TestProjectCreationJob extends ApplicationBaseTest {

    @Autowired
    JobRepository jobRepository;

    @Test
    public void basicProjectCreation() throws Exception {
        ProjectCommit projectCommit = new ProjectCommit();
        String route = AppRoutes.Jobs.createProject;
        JSONObject response = sendPost(route, projectCommit, status().isOk());

        // Step - Find Job
        String jobId = response.getString("id");

        // Step - Get Job and subscribe for updates
        createNewConnection(currentUsername)
            .subscribeToJob(currentUsername, getJob(jobId));

        // VP - Verify that current update sent
        Job message = getNextMessage(currentUsername, Job.class);
        assertThat(message).isNotNull();
        assertThat(message.getStartedAt()).isNotNull();

        // Step - Allow job to run
        Thread.sleep(500);

        // VP - Verify that job has finished.
        Job job = getJob(jobId);
        assertThat(job.getCurrentStep()).isEqualTo(3);
        assertThat(job.getCurrentProgress()).isEqualTo(100);
        assertThat(job.getStatus()).isEqualTo(JobStatus.COMPLETED);

        // Step - Assert that start is before completed.
        assert job.getCompletedAt() != null;
        int comparison = job.getCompletedAt().compareTo(job.getStartedAt());
        assertThat(comparison).isEqualTo(1);
    }

    public Job getJob(String jobIdStr) {
        UUID jobId = UUID.fromString(jobIdStr);
        Optional<Job> jobQuery = this.jobRepository.findById(jobId);
        assertThat(jobQuery.isPresent()).isTrue();
        return jobQuery.get();
    }
}
