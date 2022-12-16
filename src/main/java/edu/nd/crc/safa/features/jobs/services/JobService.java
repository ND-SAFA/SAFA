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
import edu.nd.crc.safa.features.jobs.entities.app.JobType;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.jobs.repositories.JobDbRepository;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.services.SafaUserService;

import org.springframework.batch.core.JobParameters;
import org.springframework.batch.core.JobParametersBuilder;
import org.springframework.batch.core.JobParametersInvalidException;
import org.springframework.batch.core.launch.JobLauncher;
import org.springframework.batch.core.repository.JobExecutionAlreadyRunningException;
import org.springframework.batch.core.repository.JobInstanceAlreadyCompleteException;
import org.springframework.batch.core.repository.JobRestartException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Service;

/**
 * Responsible for creating units-of-work to be used in JobController.
 */
@Service
@Scope("singleton")
public class JobService {
    /**
     * Repository for creating job entities in the database.
     */
    JobDbRepository jobDbRepository;
    /**
     * Service used to add authenticated user to job.
     */
    SafaUserService safaUserService;

    @Autowired
    public JobService(JobDbRepository jobDbRepository,
                      SafaUserService safaUserService) {
        this.jobDbRepository = jobDbRepository;
        this.safaUserService = safaUserService;
    }

    public void deleteJob(UUID jobId) {
        this.jobDbRepository.deleteById(jobId);
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
    public JobDbEntity createNewJobForUser(JobType jobType, String name, SafaUser user) {
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
    public JobDbEntity createNewJob(JobType jobType, String name) {
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
        jobDbEntity.setCompletedAt(now());
        this.jobDbRepository.save(jobDbEntity);
    }

    /**
     * Sets status of job to failed and saves it.
     *
     * @param jobDbEntity The job to fail.
     */
    public void failJob(JobDbEntity jobDbEntity) {
        jobDbEntity.setStatus(JobStatus.FAILED);
        jobDbEntity.setCurrentProgress(-1);
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
        throw new SafaError("Could not find job with id:" + jobId);
    }

    public void setJobName(JobDbEntity jobDbEntity, String newName) {
        jobDbEntity.setName(newName);
        this.jobDbRepository.save(jobDbEntity);
    }

    private Timestamp now() {
        return new Timestamp(System.currentTimeMillis());
    }

    public void executeJob(JobDbEntity jobDbEntity,
                           ServiceProvider serviceProvider,
                           AbstractJob jobCreationThread) throws
        JobExecutionAlreadyRunningException, JobRestartException,
        JobInstanceAlreadyCompleteException, JobParametersInvalidException {
        JobParameters jobParameters = new JobParametersBuilder()
            .addLong("time", System.currentTimeMillis()).toJobParameters();

        try {
            jobCreationThread.initJobData();
        } catch (Exception e) {
            e.printStackTrace();
            serviceProvider.getJobService().failJob(jobDbEntity);
            throw new SafaError("Failed to start job. %s", e.getMessage());
        }
        JobLauncher jobLauncher = serviceProvider.getJobLauncher();
        jobLauncher.run(jobCreationThread, jobParameters);
    }
}
