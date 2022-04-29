package edu.nd.crc.safa.server.controllers;

import java.util.UUID;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.api.JobSubmission;
import edu.nd.crc.safa.server.entities.api.JobType;
import edu.nd.crc.safa.server.entities.api.ProjectCommit;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.db.Job;
import edu.nd.crc.safa.server.services.JobService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * Responsible for submitting jobs and retrieving their results.
 */
@RestController
public class JobController extends BaseController {

    JobService jobService;

    @Autowired
    public JobController(ResourceBuilder resourceBuilder, JobService jobService) {
        super(resourceBuilder);
        this.jobService = jobService;
    }

    private static <T> T convertInstanceOfObject(Object o, Class<T> clazz) {
        try {
            return clazz.cast(o);
        } catch (ClassCastException e) {
            return null;
        }
    }

    @GetMapping(AppRoutes.Jobs.getJobStatus)
    public Job getJobStatus(UUID jobId) throws SafaError {
        return this.jobService.retrieveJob(jobId);
    }

    @GetMapping(AppRoutes.Jobs.getJobResult)
    public <T> T jobJobResult(UUID jobId) throws SafaError {
        throw new SafaError("Retrieving job result is under construction");
    }

    /**
     * Responsible for stopping the process running the job and cleaning up any resources.
     *
     * @param jobId The UUID for the job to stop.
     * @throws SafaError Throws error because still in construction.
     */
    @DeleteMapping(AppRoutes.Jobs.deleteJob)
    public void stopJob(UUID jobId) throws SafaError {
        throw new SafaError("Stopping jobs is under construction");
    }

    @PostMapping(AppRoutes.Jobs.createNewJob)
    public Job createNewJob(JobSubmission jobSubmission) throws SafaError {
        JobType jobType = jobSubmission.getJobType();
        switch (jobType) {
            case PROJECT_CREATION:
                ProjectCommit projectCommit = convertInstanceOfObject(jobSubmission.getPayload(), ProjectCommit.class);
                
                throw new SafaError("Stopping jobs is under construction");
            default:
                throw new RuntimeException("Job type not implemented:" + jobType);
        }
    }
}
