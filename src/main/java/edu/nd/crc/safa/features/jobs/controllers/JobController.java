package edu.nd.crc.safa.features.jobs.controllers;

import java.util.List;
import java.util.UUID;
import javax.validation.Valid;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.builders.CreateProjectByJsonJobBuilder;
import edu.nd.crc.safa.features.jobs.builders.GenerateLinksJobBuilder;
import edu.nd.crc.safa.features.jobs.builders.UpdateProjectByFlatFileJobBuilder;
import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
import edu.nd.crc.safa.features.jobs.services.JobService;
import edu.nd.crc.safa.features.notifications.builders.EntityChangeBuilder;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.tgen.entities.TraceGenerationRequest;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

/**
 * Responsible for submitting jobs and retrieving their results.
 */
@RestController
public class JobController extends BaseController {

    private final JobService jobService;

    @Autowired
    public JobController(ResourceBuilder resourceBuilder,
                         ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
        this.jobService = serviceProvider.getJobService();
    }

    /**
     * Returns the list of jobs created by the authenticated user.
     *
     * @return The list of jobs created by user.
     * @throws SafaError If authentication error occurs.
     */
    @GetMapping(AppRoutes.Jobs.Meta.GET_JOBS)
    public List<JobAppEntity> getUserJobs() throws SafaError {
        return this.jobService.retrieveCurrentUserJobs();
    }

    /**
     * Responsible for stopping the process running the job and cleaning up any resources.
     *
     * @param jobId The UUID for the job to stop.
     * @throws SafaError Throws error because still in construction.
     */
    @DeleteMapping(AppRoutes.Jobs.Meta.DELETE_JOB)
    public void deleteJob(@PathVariable UUID jobId) throws SafaError {
        this.jobService.deleteJob(jobId);
        this.serviceProvider.getNotificationService().broadcastChange(
            EntityChangeBuilder
                .create(jobId)
                .withJobDelete(jobId)
        );
    }

    /**
     * Parses given job payload by the jobType and returns the job created.
     *
     * @param versionId The project version to save the entities to.
     * @param files     The flat files to be parsed and uploaded.
     * @return The current status of the job created.
     * @throws SafaError Throws error if job failed to start or is under construction.
     */
    @PostMapping(AppRoutes.Jobs.Projects.UPDATE_PROJECT_VIA_FLAT_FILES)
    @ResponseStatus(HttpStatus.CREATED)
    public JobAppEntity flatFileProjectUpdateJob(@PathVariable UUID versionId,
                                                 @RequestParam MultipartFile[] files) throws Exception {
        UpdateProjectByFlatFileJobBuilder updateProjectByFlatFileJobBuilder = new UpdateProjectByFlatFileJobBuilder(
            serviceProvider,
            versionId, files);
        return updateProjectByFlatFileJobBuilder.perform();
    }

    /**
     * Creates a project by saving project entities.
     *
     * @param projectAppEntity The project entities to save (e.g. artifacts, traces.
     * @return {@link JobAppEntity} The job created for this task.
     * @throws Exception If an error occurs while setting up job.
     */
    @PostMapping(AppRoutes.Jobs.Projects.CREATE_PROJECT_VIA_JSON)
    public JobAppEntity createProjectFromJSON(@RequestBody ProjectAppEntity projectAppEntity) throws Exception {
        CreateProjectByJsonJobBuilder createProjectByJsonJobBuilder = new CreateProjectByJsonJobBuilder(
            serviceProvider, projectAppEntity);
        return createProjectByJsonJobBuilder.perform();
    }

    /**
     * Creates a job for generating trace links between source and target artifacts with specified method.
     *
     * @param request Request identifying source and target artifacts along with the method to generate links with.
     * @return The {@link JobAppEntity} create for this job.
     * @throws Exception If an error occurs while starting job.
     */
    @PostMapping(AppRoutes.Jobs.Traces.GENERATE)
    public JobAppEntity generateTraceLinks(@RequestBody @Valid TraceGenerationRequest request) throws Exception {
        ProjectVersion projectVersion = resourceBuilder.fetchVersion(request.getProjectVersion().getVersionId())
            .withEditVersion(); // Makes sure all persistent properties are available
        request.setProjectVersion(projectVersion);
        GenerateLinksJobBuilder jobBuilder = new GenerateLinksJobBuilder(this.serviceProvider, request);
        return jobBuilder.perform();
    }
}
