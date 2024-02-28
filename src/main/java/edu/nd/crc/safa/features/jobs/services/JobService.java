package edu.nd.crc.safa.features.jobs.services;

import java.sql.Timestamp;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.jobs.entities.app.AbstractJob;
import edu.nd.crc.safa.features.jobs.entities.app.JobAppEntity;
import edu.nd.crc.safa.features.jobs.entities.app.JobStatus;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.jobs.repositories.JobDbRepository;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.app.SafaItemNotFoundError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.services.SafaUserService;

import lombok.AllArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.batch.core.JobParameters;
import org.springframework.batch.core.JobParametersBuilder;
import org.springframework.batch.core.JobParametersInvalidException;
import org.springframework.batch.core.launch.JobLauncher;
import org.springframework.batch.core.repository.JobExecutionAlreadyRunningException;
import org.springframework.batch.core.repository.JobInstanceAlreadyCompleteException;
import org.springframework.batch.core.repository.JobRestartException;
import org.springframework.context.annotation.Scope;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;

/**
 * Responsible for creating units-of-work to be used in JobController.
 */
@AllArgsConstructor
@Service
@Scope("singleton")
public class JobService {
    /**
     * Logger used for job services.
     */
    private static final Logger logger = LoggerFactory.getLogger(JobService.class);
    private final JobDbRepository jobDbRepository;
    private final SafaUserService safaUserService;

    public void removeProjectFromJobs(Project project) {
        List<JobDbEntity> projectJobs = getJobDbEntitiesInProjects(List.of(project));
        projectJobs.forEach(jobDbEntity -> jobDbEntity.setProject(null));
        this.jobDbRepository.saveAll(projectJobs);
    }

    /**
     * Deletes the job with given ID. Terminates any task associated with the job.
     *
     * @param jobId The ID of the job.
     * @return The deleted job entity.
     */
    public JobDbEntity deleteJob(UUID jobId) {
        Optional<JobDbEntity> optionalJobDbEntity = this.jobDbRepository.findById(jobId);
        if (optionalJobDbEntity.isEmpty()) {
            return null;
        }
        JobDbEntity jobDbEntity = optionalJobDbEntity.get();
        this.jobDbRepository.delete(jobDbEntity);
        return jobDbEntity;
    }

    /**
     * Returns list of the jobs the current user has created.
     *
     * @return List of jobs created by currently authenticated user.
     */
    public List<JobAppEntity> retrieveCurrentUserJobs() {
        SafaUser currentUser = this.safaUserService.getCurrentUser();
        return this.jobDbRepository
            .findByUserOrderByLastUpdatedAtDesc(currentUser)
            .stream()
            .map(JobAppEntity::createFromJob)
            .collect(Collectors.toList());
    }

    /**
     * Retrieves all jobs associated with project.
     *
     * @param project The project whose jobs are retrieved.
     * @return The list of jobs.
     */
    public List<JobAppEntity> getProjectJobs(Project project) {
        return this.getJobsInProjects(List.of(project));
    }

    /**
     * Creates new job with:
     * - given authenticated user as creator
     * - status as In Progress
     * - current progress equals 0
     *
     * @param jobType The type of job being performed.
     * @param name    The name of the job.
     * @param user    The user to create the job for
     * @return The saved job db entity.
     */
    public JobDbEntity createNewJobForUser(Class<? extends AbstractJob> jobType, String name, SafaUser user) {
        JobDbEntity jobDbEntity = new JobDbEntity(
            user,
            name,
            jobType,
            JobStatus.IN_PROGRESS,
            now(),
            now(),
            null,
            0,
            -1
        );
        this.jobDbRepository.save(jobDbEntity);
        return jobDbEntity;
    }

    /**
     * Creates new job with:
     * - current authenticated user as creator
     * - status as In Progress
     * - current progress equals 0
     *
     * @param jobType The type of job being performed.
     * @param name    The name of the job.
     * @return The saved job db entity.
     */
    public JobDbEntity createNewJob(Class<? extends AbstractJob> jobType, String name) {
        SafaUser currentUser = this.safaUserService.getCurrentUser();
        return createNewJobForUser(jobType, name, currentUser);
    }

    /**
     * Saves job with lastUpdated date at time of save.
     *
     * @param jobDbEntity The job whose lastUpdated property is being modified.
     * @param nSteps      The number of steps in job.
     */
    public void startStep(JobDbEntity jobDbEntity, int nSteps) {
        jobDbEntity.incrementStep();
        jobDbEntity.incrementProgress(nSteps - 1); // excluding done step
        this.jobDbRepository.save(jobDbEntity);
    }

    /**
     * Saves job with lastUpdated date at time of save.
     *
     * @param jobDbEntity The job whose lastUpdated property is being modified.
     * @param stepNum     The index of the step we're starting.
     * @param nSteps      The number of steps in job.
     */
    public void startStep(JobDbEntity jobDbEntity, int stepNum, int nSteps) {
        jobDbEntity.setCurrentStep(stepNum);
        jobDbEntity.incrementProgress(nSteps - 1); // excluding done step
        this.jobDbRepository.save(jobDbEntity);
    }

    /**
     * Moves job to next step and saves job.
     *
     * @param jobDbEntity The job to update its step.
     */
    public void endStep(JobDbEntity jobDbEntity) {
        this.jobDbRepository.save(jobDbEntity);
    }

    /**
     * Marks status as complete, sets progress to 100, and sets completed at property.
     *
     * @param jobDbEntity The job to complete.
     */
    public void completeJob(JobDbEntity jobDbEntity) {
        jobDbEntity.setStatus(JobStatus.COMPLETED);
        jobDbEntity.setCurrentProgress(100);
        endJob(jobDbEntity);
    }

    /**
     * Sets status of job to failed and saves it.
     *
     * @param jobDbEntity The job to fail.
     */
    public void failJob(JobDbEntity jobDbEntity) {
        jobDbEntity.setStatus(JobStatus.FAILED);
        jobDbEntity.setCurrentProgress(-1);
        endJob(jobDbEntity);
    }

    private void endJob(JobDbEntity jobDbEntity) {
        jobDbEntity.setCompletedAt(now());
        this.jobDbRepository.save(jobDbEntity);
    }

    /**
     * Returns job database entity with given id.
     *
     * @param jobId The id of the job to retrieve.
     * @return The job database entity.
     * @throws SafaError Throws error is jobs with id not found.
     */
    public JobDbEntity getJobById(UUID jobId) throws SafaError {
        Optional<JobDbEntity> jobOption = this.jobDbRepository.findById(jobId);
        if (jobOption.isPresent()) {
            return jobOption.get();
        }
        throw new SafaItemNotFoundError("Could not find job with id: " + jobId);
    }

    public void setJobName(JobDbEntity jobDbEntity, String newName) {
        jobDbEntity.setName(newName);
        this.jobDbRepository.save(jobDbEntity);
    }

    private Timestamp now() {
        return new Timestamp(System.currentTimeMillis());
    }

    public void executeJob(ServiceProvider serviceProvider, AbstractJob job) throws
        JobExecutionAlreadyRunningException, JobRestartException,
        JobInstanceAlreadyCompleteException, JobParametersInvalidException {

        JobParameters jobParameters = new JobParametersBuilder()
            .addLong("time", System.currentTimeMillis()).toJobParameters();

        JobLauncher jobLauncher = serviceProvider.getJobLauncher();
        job.setAuthentication(SecurityContextHolder.getContext().getAuthentication());
        jobLauncher.run(job, jobParameters);
    }

    /**
     * Sets the current task ID on given job.
     *
     * @param jobDbEntity The job to update.
     * @param taskId      The task ID to add to job.
     */
    public void setJobTask(JobDbEntity jobDbEntity, UUID taskId) {
        jobDbEntity.setTaskId(taskId);
        this.jobDbRepository.save(jobDbEntity);
    }

    /**
     * Returns the jobs associated with projects.
     *
     * @param projects The list of projects whose collective jobs are returned sorted by last updated.
     * @return The list of jobs.
     */
    public List<JobAppEntity> getJobsInProjects(List<Project> projects) {
        return getJobDbEntitiesInProjects(projects)
            .stream()
            .map(JobAppEntity::createFromJob)
            .collect(Collectors.toList());
    }

    private List<JobDbEntity> getJobDbEntitiesInProjects(List<Project> projects) {
        List<UUID> projectIds = projects.stream().map(Project::getProjectId).collect(Collectors.toList());
        return this.jobDbRepository.findByProjectProjectIdInOrderByLastUpdatedAtDesc(projectIds);
    }
}
