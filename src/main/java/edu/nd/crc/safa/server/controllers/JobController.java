package edu.nd.crc.safa.server.controllers;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.api.jobs.FlatFileProjectCreationJob;
import edu.nd.crc.safa.server.entities.api.jobs.JobType;
import edu.nd.crc.safa.server.entities.app.JobAppEntity;
import edu.nd.crc.safa.server.entities.db.JobDbEntity;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.projects.ProjectRepository;
import edu.nd.crc.safa.server.services.EntityVersionService;
import edu.nd.crc.safa.server.services.NotificationService;
import edu.nd.crc.safa.server.services.ProjectService;
import edu.nd.crc.safa.server.services.ServiceProvider;
import edu.nd.crc.safa.server.services.jobs.JobService;
import edu.nd.crc.safa.server.services.retrieval.AppEntityRetrievalService;

import org.springframework.batch.core.JobParametersInvalidException;
import org.springframework.batch.core.repository.JobExecutionAlreadyRunningException;
import org.springframework.batch.core.repository.JobInstanceAlreadyCompleteException;
import org.springframework.batch.core.repository.JobRestartException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.task.TaskExecutor;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

/**
 * Responsible for submitting jobs and retrieving their results.
 */
@RestController
public class JobController extends BaseController {

    JobService jobService;
    EntityVersionService entityVersionService;
    ProjectService projectService;
    ProjectRepository projectRepository; //TODO: Extract into service?
    AppEntityRetrievalService appEntityRetrievalService;
    NotificationService notificationService;
    TaskExecutor taskExecutor;
    ServiceProvider serviceProvider;

    @Autowired
    public JobController(ResourceBuilder resourceBuilder,
                         JobService jobService,
                         EntityVersionService entityVersionService,
                         ProjectService projectService,
                         ProjectRepository projectRepository,
                         AppEntityRetrievalService appEntityRetrievalService,
                         NotificationService notificationService,
                         TaskExecutor taskExecutor,
                         ServiceProvider serviceProvider) {
        super(resourceBuilder);
        this.jobService = jobService;
        this.entityVersionService = entityVersionService;
        this.projectService = projectService;
        this.projectRepository = projectRepository;
        this.appEntityRetrievalService = appEntityRetrievalService;
        this.notificationService = notificationService;
        this.taskExecutor = taskExecutor;
        this.serviceProvider = serviceProvider;
    }

    @GetMapping(AppRoutes.Jobs.getJobs)
    public List<JobAppEntity> getJobStatus() throws SafaError {
        return this.jobService.retrieveCurrentUserJobs();
    }

    /**
     * Responsible for stopping the process running the job and cleaning up any resources.
     *
     * @param jobId The UUID for the job to stop.
     * @throws SafaError Throws error because still in construction.
     */
    @DeleteMapping(AppRoutes.Jobs.deleteJob)
    public void deleteJob(@PathVariable UUID jobId) throws SafaError {
        //TODO: Find a way to stop jobs
        this.jobService.deleteJob(jobId);
    }

    /**
     * Parses given job payload by the jobType and returns the job created.
     *
     * @param versionId The project version to save the entities to.
     * @param files     The flat files to be parsed and uploaded.
     * @return The current status of the job created.
     * @throws SafaError Throws error if job failed to start or is under construction.
     */
    @PostMapping(AppRoutes.Jobs.flatFileProjectUpdateJob)
    @ResponseStatus(HttpStatus.CREATED)
    public JobAppEntity flatFileProjectUpdateJob(@PathVariable UUID versionId,
                                                 @RequestParam MultipartFile[] files) throws SafaError,
        JobInstanceAlreadyCompleteException, JobExecutionAlreadyRunningException,
        JobParametersInvalidException, JobRestartException {
        // Step 1 - Fetch version and assert permissions
        ProjectVersion projectVersion = this.resourceBuilder.fetchVersion(versionId).withEditVersion();

        // Step 2 - Create new job
        String name = "Uploading flat files to: " + projectVersion.getProject().getName();
        JobDbEntity jobDbEntity = this.jobService.createNewJob(JobType.FLAT_FILE_PROJECT_CREATION, name);

        // Step 3 - Create job worker
        FlatFileProjectCreationJob jobCreationThread = new FlatFileProjectCreationJob(jobDbEntity,
            serviceProvider,
            projectVersion,
            files);

        jobService.executeJob(jobDbEntity, serviceProvider, jobCreationThread);

        // Step 4 - Create job response
        return JobAppEntity.createFromJob(jobDbEntity);
    }
}
