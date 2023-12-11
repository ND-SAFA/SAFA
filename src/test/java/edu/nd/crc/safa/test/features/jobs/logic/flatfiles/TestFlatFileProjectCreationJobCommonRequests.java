package edu.nd.crc.safa.test.features.jobs.logic.flatfiles;

import static org.hibernate.validator.internal.util.Contracts.assertNotNull;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.config.ProjectPaths;
import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.test.features.jobs.base.AbstractUpdateProjectViaFlatFileTestCommonRequests;
import edu.nd.crc.safa.test.features.jobs.base.JobTestService;
import edu.nd.crc.safa.test.services.requests.CommonProjectRequests;

import org.junit.jupiter.api.Test;

class TestFlatFileProjectCreationJobCommonRequests extends AbstractUpdateProjectViaFlatFileTestCommonRequests {

    int N_STEPS = 5;

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
        UUID jobId = updateProjectViaFlatFiles(ProjectPaths.Resources.Tests.DefaultProject.V1);

        // Step - Get Job and subscribe for updates
        this.rootBuilder
            .notifications(n -> n
                .initializeUser(getCurrentUser(), getToken(getCurrentUser()))
                .subscribeToJob(getCurrentUser(), jobService.getJobById(jobId)));
        // VP - Verify that job has finished.
        JobTestService.verifyJobWasCompleted(serviceProvider, jobId, N_STEPS);

        // VP - Verify that job is associated with project
        JobDbEntity job = this.serviceProvider.getJobService().getJobById(jobId);
        assertNotNull(job.getProject());
        Project project = job.getProject();

        // VP - Verify that project job is logged.
        List<JobAppEntity> projectJobs = CommonProjectRequests.getProjectJobs(project);

        // VP - Verify that all entities were created
        verifyDefaultProjectEntities(projectVersion.getProject());
    }
}
