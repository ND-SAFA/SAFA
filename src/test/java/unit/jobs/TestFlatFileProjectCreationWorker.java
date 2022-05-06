package unit.jobs;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.server.entities.app.JobStatus;
import edu.nd.crc.safa.server.entities.db.Job;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.JobRepository;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import unit.flatfile.FlatFileBaseTest;

public class TestFlatFileProjectCreationWorker extends FlatFileBaseTest {

    @Autowired
    JobRepository jobRepository;

    @Test
    public void uploadBeforeProject() throws Exception {

        // Step - Create project
        String projectName = "test-before-files";
        ProjectVersion projectVersion = dbEntityBuilder
            .newProject(projectName)
            .newVersionWithReturn(projectName);

        // Step - Send request to upload flat files to project
        JSONObject response = uploadFlatFilesToVersion(projectVersion,
            ProjectPaths.PATH_TO_BEFORE_FILES,
            AppRoutes.Jobs.flatFileProjectUpdateJob);

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
        assertThat(job.getCurrentStep()).isEqualTo(6);
        assertThat(job.getCurrentProgress()).isEqualTo(100);
        assertThat(job.getStatus()).isEqualTo(JobStatus.COMPLETED);

        // Step - Assert that start is before completed.
        assert job.getCompletedAt() != null;
        int comparison = job.getCompletedAt().compareTo(job.getStartedAt());
        assertThat(comparison).isEqualTo(1);

        // VP - Verify that all entities were created
        verifyBeforeEntities(projectVersion.getProject());
    }

    public Job getJob(String jobIdStr) {
        UUID jobId = UUID.fromString(jobIdStr);
        Optional<Job> jobQuery = this.jobRepository.findById(jobId);
        assertThat(jobQuery.isPresent()).isTrue();
        return jobQuery.get();
    }
}
