package edu.nd.crc.safa.features.jobs.logging.controllers;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.logging.entities.JobLogEntryAppEntity;
import edu.nd.crc.safa.features.jobs.logging.services.JobLoggingService;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.services.SafaUserService;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

/**
 * Allows for retrieving saved logs for jobs.
 */
@RestController
public class JobLoggingController extends BaseController {

    private final JobLoggingService jobLoggingService;

    private final SafaUserService safaUserService;

    public JobLoggingController(ResourceBuilder resourceBuilder, ServiceProvider serviceProvider,
                                JobLoggingService jobLoggingService, SafaUserService safaUserService) {
        super(resourceBuilder, serviceProvider);
        this.jobLoggingService = jobLoggingService;
        this.safaUserService = safaUserService;
    }

    /**
     * Get all logs for a given job. The return type is a list of lists, where the index in the
     * outer list corresponds to the step index, and the inner list is sorted by timestamp.
     *
     * @param jobId The ID of the job.
     * @return All logs associated with the job.
     * @throws SafaError If there is a problem accessing the job or its logs.
     */
    @GetMapping(AppRoutes.Jobs.Logs.BY_JOB_ID)
    public List<List<JobLogEntryAppEntity>> getLogsForJob(@PathVariable UUID jobId) throws SafaError {
        SafaUser currentUser = this.safaUserService.getCurrentUser();
        return jobLoggingService.getJsonLogEntitiesForJob(jobId, currentUser);
    }

    /**
     * Get all logs for a step of a job. No attempt is made to validate the step number. If it is
     * out of range, an empty list will be returned.
     *
     * @param jobId The ID of the job.
     * @param stepNum The index of the step. 0-indexed.
     * @return The logs for that job step, sorted by timestamp.
     * @throws SafaError If there is a problem accessing the job or its logs.
     */
    @GetMapping(AppRoutes.Jobs.Logs.BY_JOB_ID_AND_STEP_NUM)
    public List<JobLogEntryAppEntity> getLogsForJob(@PathVariable UUID jobId,
                                                    @PathVariable short stepNum) throws SafaError {
        SafaUser currentUser = this.safaUserService.getCurrentUser();
        return jobLoggingService.getJsonLogEntitiesForJobStep(jobId, currentUser, stepNum);
    }
}
