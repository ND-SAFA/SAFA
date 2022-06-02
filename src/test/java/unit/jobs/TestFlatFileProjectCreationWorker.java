package unit.jobs;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.Arrays;
import java.util.UUID;

import edu.nd.crc.safa.server.entities.app.JobStatus;
import edu.nd.crc.safa.server.entities.db.JobDbEntity;

import org.junit.jupiter.api.Test;

public class TestFlatFileProjectCreationWorker extends JobBaseTest {
    
    /*
     * Tests that uploading default project as job completes.
     *
     * @throws Exception Throws exception if:
     *                   1. Upload fails
     *                   2. Connection to job messages fails
     *                   3. Receiving web socket messages
     *                   4. Sleeping thread to wait for job to finish fails.
     */
    @Test
    public void testDefaultProjectCompletes() throws Exception {

        // Step - Find Job
        UUID jobId = createJobFromDefaultProject();

        // Step - Get Job and subscribe for updates
        createNewConnection(currentUsername)
            .subscribeToJob(currentUsername, jobService.getJobById(jobId));

        // Step - Allow job to run
        Thread.sleep(5000);

        // VP - Verify that job has finished.
        JobDbEntity jobDbEntity = jobService.getJobById(jobId);
        assertThat(jobDbEntity.getCurrentStep()).isGreaterThanOrEqualTo(0);
        assertThat(jobDbEntity.getCurrentProgress()).isGreaterThanOrEqualTo(0);
        assertThat(jobDbEntity.getStatus()).isIn(Arrays.asList(JobStatus.IN_PROGRESS, JobStatus.COMPLETED));

        // Step - Assert that start is before completed.
        assert jobDbEntity.getCompletedAt() != null;
        int comparison = jobDbEntity.getCompletedAt().compareTo(jobDbEntity.getStartedAt());
        assertThat(comparison).isEqualTo(1);

        // Step - Assert that lastUpdatedBy is after start.
        comparison = jobDbEntity.getLastUpdatedAt().compareTo(jobDbEntity.getStartedAt());
        assertThat(comparison).isEqualTo(1);

        // VP - Verify that all entities were created
        verifyBeforeEntities(projectVersion.getProject());
    }
}
