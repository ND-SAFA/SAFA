package features.jobs.logic.flatfiles;

import java.util.UUID;

import features.jobs.base.AbstractFlatFileJobTest;
import features.jobs.base.JobTestService;
import org.junit.jupiter.api.Test;

class TestProjectCreationWorkerFlatFile extends AbstractFlatFileJobTest {

    int N_STEPS = 4;

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
    void testDefaultProjectCompletes() throws Exception {

        // Step - Find Job
        UUID jobId = createJobForDefaultProject();

        // Step - Get Job and subscribe for updates
        createNewConnection(defaultUser).subscribeToJob(defaultUser, jobService.getJobById(jobId));

        // VP - Verify that job has finished.
        JobTestService.verifyJobWasCompleted(serviceProvider, jobId, N_STEPS);

        // VP - Verify that all entities were created
        verifyDefaultProjectEntities(projectVersion.getProject());
    }
}
