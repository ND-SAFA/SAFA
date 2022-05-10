package unit.jobs;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.UUID;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.server.entities.app.JobStatus;
import edu.nd.crc.safa.server.entities.db.JobDbEntity;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.services.JobService;
import edu.nd.crc.safa.server.services.NotificationService;

import org.json.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import unit.flatfile.FlatFileBaseTest;

public class TestFlatFileProjectCreationWorker extends FlatFileBaseTest {

    @Autowired
    JobService jobService;

    @Autowired
    NotificationService notificationService;

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
        UUID jobId = UUID.fromString(response.getString("id"));

        // Step - Get Job and subscribe for updates
        createNewConnection(currentUsername)
            .subscribeToJob(currentUsername, jobService.getJobById(jobId));

        // VP - Verify that current update sent
        JobDbEntity message = getNextMessage(currentUsername, JobDbEntity.class);
        assertThat(message).isNotNull();
        assertThat(message.getCurrentStep()).isEqualTo(1);

        // Step - Allow job to run
        Thread.sleep(500);

        // VP - Verify that job has finished.
        JobDbEntity jobDbEntity = jobService.getJobById(jobId);
        assertThat(jobDbEntity.getCurrentStep()).isEqualTo(6);
        assertThat(jobDbEntity.getCurrentProgress()).isEqualTo(100);
        assertThat(jobDbEntity.getStatus()).isEqualTo(JobStatus.COMPLETED);

        // Step - Assert that start is before completed.
        assert jobDbEntity.getCompletedAt() != null;
        int comparison = jobDbEntity.getCompletedAt().compareTo(jobDbEntity.getStartedAt());
        assertThat(comparison).isEqualTo(1);

        // VP - Verify that all entities were created
        verifyBeforeEntities(projectVersion.getProject());
    }
}
