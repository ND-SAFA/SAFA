package edu.nd.crc.safa.features.jobs.controllers;

import java.util.List;
import java.util.Optional;
import java.util.Set;
import java.util.UUID;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.BaseController;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.generation.api.GenApi;
import edu.nd.crc.safa.features.generation.tgen.entities.TGenRequestAppEntity;
import edu.nd.crc.safa.features.jobs.builders.CreateProjectByFlatFileJobBuilder;
import edu.nd.crc.safa.features.jobs.builders.CreateProjectByJsonJobBuilder;
import edu.nd.crc.safa.features.jobs.builders.GenerateLinksJobBuilder;
import edu.nd.crc.safa.features.jobs.builders.UpdateProjectByFlatFileJobBuilder;
import edu.nd.crc.safa.features.jobs.entities.app.CreateProjectByJsonPayload;
import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.jobs.services.JobService;
import edu.nd.crc.safa.features.notifications.builders.EntityChangeBuilder;
import edu.nd.crc.safa.features.permissions.MissingPermissionException;
import edu.nd.crc.safa.features.permissions.checks.billing.HasUnlimitedCreditsCheck;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.features.permissions.entities.SimplePermission;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.services.SafaUserService;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.utilities.JobUtil;

import jakarta.validation.Valid;
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
    private final SafaUserService safaUserService;
    private final GenApi genApi;

    @Autowired
    public JobController(ResourceBuilder resourceBuilder,
                         ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
        this.jobService = serviceProvider.getJobService();
        this.safaUserService = serviceProvider.getSafaUserService();
        this.genApi = serviceProvider.getGenApi();
    }

    /**
     * Returns the list of jobs created by the authenticated user.
     *
     * @return The list of jobs created by user.
     * @throws SafaError If authentication error occurs.
     */
    @GetMapping(AppRoutes.Jobs.Meta.GET_USER_JOBS)
    public List<JobAppEntity> getUserJobs() throws SafaError {
        return this.jobService.retrieveCurrentUserJobs();
    }

    /**
     * Returns the list of jobs associated with project.
     *
     * @param projectId The ID of project.
     * @return The list of jobs created by user.
     * @throws SafaError If authentication error occurs.
     */
    @GetMapping(AppRoutes.Jobs.Meta.GET_PROJECT_JOBS)
    public List<JobAppEntity> getProjectJobs(@PathVariable UUID projectId) throws SafaError {
        ServiceProvider serviceProvider = this.getServiceProvider();
        SafaUser user = serviceProvider.getSafaUserService().getCurrentUser();
        Project project = this.getResourceBuilder().fetchProject(projectId)
            .withPermission(ProjectPermission.VIEW, user).get();
        return this.jobService.getProjectJobs(project);
    }

    /**
     * Responsible for stopping the process running the job and cleaning up any resources.
     *
     * @param jobId The UUID for the job to stop.
     * @throws SafaError Throws error because still in construction.
     */
    @DeleteMapping(AppRoutes.Jobs.Meta.DELETE_JOB)
    public void deleteJob(@PathVariable UUID jobId) throws SafaError {
        SafaUser user = getCurrentUser();
        JobDbEntity job = jobService.getJobById(jobId);
        if (job != null && !job.getUser().equals(user)) {
            throw new MissingPermissionException((SimplePermission) () -> "delete_job");
        }

        JobDbEntity jobDbEntity = this.jobService.deleteJob(jobId);
        if (jobDbEntity != null) {
            UUID taskId = jobDbEntity.getTaskId();
            this.genApi.cancelJob(taskId);
        }
        getServiceProvider().getNotificationService().broadcastChange(
            EntityChangeBuilder
                .create(user, jobDbEntity)
                .withJobDelete(jobDbEntity)
        );
    }

    /**
     * Parses given job payload by the jobType and returns the job created.
     *
     * @param versionId     The project version to save the entities to.
     * @param files         The flat files to be parsed and uploaded.
     * @param summarize     Whether to summarize code artifacts on upload.
     * @param asCompleteSet Whether the uploaded files contain the complete set of project artifacts.
     * @return The current status of the job created.
     * @throws SafaError Throws error if job failed to start or is under construction.
     */
    @PostMapping(AppRoutes.Jobs.Projects.UPDATE_PROJECT_VIA_FLAT_FILES)
    @ResponseStatus(HttpStatus.CREATED)
    public JobAppEntity flatFileProjectUpdateJob(
        @PathVariable UUID versionId,
        @RequestParam Optional<List<MultipartFile>> files,
        @RequestParam(required = false, defaultValue = "false") boolean summarize,
        @RequestParam(required = false, defaultValue = "false") boolean asCompleteSet)
        throws Exception {
        SafaUser user = safaUserService.getCurrentUser();
        ProjectVersion projectVersion = getResourceBuilder()
            .fetchVersion(versionId)
            .withPermission(ProjectPermission.EDIT_DATA, user)
            .get();
        UpdateProjectByFlatFileJobBuilder jobBuilder =
            new UpdateProjectByFlatFileJobBuilder(
                user,
                getServiceProvider(),
                projectVersion,
                files.orElseGet(JobUtil::defaultFileListSupplier),
                summarize,
                asCompleteSet);

        return jobBuilder.perform();
    }

    /**
     * Create a new project via flat file upload.
     *
     * @param files       The flat files to be parsed and uploaded.
     * @param name        The name of the new project
     * @param description The description for the new project
     * @param summarize   Whether to summarize code artifacts on upload.
     * @param teamId      Optional ID of the team to own the project.
     * @param orgId       Optional ID of the org to own the project
     * @return The current status of the job created.
     * @throws SafaError Throws error if job failed to start or is under construction.
     */
    @PostMapping(AppRoutes.Jobs.Projects.PROJECT_BULK_UPLOAD)
    @ResponseStatus(HttpStatus.CREATED)
    public JobAppEntity flatFileProjectCreationJob(
        @RequestParam Optional<List<MultipartFile>> files,
        @RequestParam String name,
        @RequestParam String description,
        @RequestParam(required = false, defaultValue = "false") boolean summarize,
        @RequestParam(required = false) UUID teamId,
        @RequestParam(required = false) UUID orgId)
        throws Exception {

        CreateProjectByFlatFileJobBuilder jobBuilder =
            new CreateProjectByFlatFileJobBuilder(
                getServiceProvider(),
                files.orElseGet(JobUtil::defaultFileListSupplier),
                safaUserService.getCurrentUser(),
                name,
                description,
                summarize,
                teamId,
                orgId);

        return jobBuilder.perform();
    }

    /**
     * Creates a project by saving project entities.
     *
     * @param payload The project entities to save (e.g. artifacts, traces) and traces to generate.
     * @return {@link JobAppEntity} The job created for this task.
     * @throws Exception If an error occurs while setting up job.
     */
    @PostMapping(AppRoutes.Jobs.Projects.CREATE_PROJECT_VIA_JSON)
    public JobAppEntity createProjectFromJSON(@RequestBody @Valid CreateProjectByJsonPayload payload) throws Exception {
        // Step - Create and start job.
        SafaUser requester = safaUserService.getCurrentUser();
        CreateProjectByJsonJobBuilder createProjectByJsonJobBuilder = new CreateProjectByJsonJobBuilder(
            requester,
            getServiceProvider(),
            payload.getProject(),
            payload.getRequests()
        );
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
    public JobAppEntity generateTraceLinks(@RequestBody @Valid TGenRequestAppEntity request) throws Exception {
        // Step - Check permissions and retrieve persistent properties
        UUID versionId = request.getProjectVersion().getVersionId();
        SafaUser user = safaUserService.getCurrentUser();
        ProjectVersion projectVersion = getResourceBuilder()
            .fetchVersion(versionId)
            .asUser(user)
            .withPermissions(Set.of(ProjectPermission.GENERATE, ProjectPermission.EDIT_DATA))
            .withAdditionalCheck(new HasUnlimitedCreditsCheck())
            .get();
        request.setProjectVersion(projectVersion);

        // Step - Create and start job.
        GenerateLinksJobBuilder jobBuilder = new GenerateLinksJobBuilder(user, getServiceProvider(), request);
        return jobBuilder.perform();
    }
}
