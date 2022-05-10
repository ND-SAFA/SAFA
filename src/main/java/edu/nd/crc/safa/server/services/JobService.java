package edu.nd.crc.safa.server.services;

import java.sql.Timestamp;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;
import javax.annotation.PostConstruct;

import edu.nd.crc.safa.server.authentication.SafaUserService;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.api.jobs.JobType;
import edu.nd.crc.safa.server.entities.app.JobDbEntityAppEntity;
import edu.nd.crc.safa.server.entities.app.JobStatus;
import edu.nd.crc.safa.server.entities.db.JobDbEntity;
import edu.nd.crc.safa.server.entities.db.SafaUser;
import edu.nd.crc.safa.server.repositories.JobDbRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
 * Responsible for creating units-of-work to be used in JobController.
 */
@Service
public class JobService {

    private static JobService instance;
    JobDbRepository jobDbRepository;
    SafaUserService safaUserService;

    @Autowired
    public JobService(JobDbRepository jobDbRepository, SafaUserService safaUserService) {
        this.jobDbRepository = jobDbRepository;
        this.safaUserService = safaUserService;
    }

    public static JobService getInstance() {
        return instance;
    }

    public void deleteJob(UUID jobId) {
        this.jobDbRepository.deleteById(jobId);
    }

    public List<JobDbEntityAppEntity> retrieveCurrentUserJobs() throws SafaError {
        SafaUser currentUser = this.safaUserService.getCurrentUser();
        return this.jobDbRepository
            .findByUser(currentUser)
            .stream()
            .map(j -> {
                try {
                    return JobDbEntityAppEntity.createFromJob(j);
                } catch (IllegalAccessException e) {
                    e.printStackTrace();
                    return null;
                }
            })
            .filter(Objects::nonNull)
            .collect(Collectors.toList());
    }

    public JobDbEntity createNewJob(JobType jobType, String name) {
        SafaUser currentUser = this.safaUserService.getCurrentUser();
        JobDbEntity jobDbEntity = new JobDbEntity(
            currentUser,
            name,
            jobType,
            JobStatus.IN_PROGRESS,
            now(),
            now(),
            null,
            0,
            0
        );
        this.jobDbRepository.save(jobDbEntity);
        return jobDbEntity;
    }

    public void startStep(JobDbEntity jobDbEntity) {
        jobDbEntity.setLastUpdatedAt(now());
        this.jobDbRepository.save(jobDbEntity);
    }

    public void endStep(JobDbEntity jobDbEntity) {
        jobDbEntity.incrementStep();
        jobDbEntity.setLastUpdatedAt(now());
        this.jobDbRepository.save(jobDbEntity);
    }

    public void completeJob(JobDbEntity jobDbEntity) {
        jobDbEntity.setStatus(JobStatus.COMPLETED);
        jobDbEntity.setCurrentProgress(100);
        jobDbEntity.setCompletedAt(now());
        jobDbEntity.setLastUpdatedAt(now());
        this.jobDbRepository.save(jobDbEntity);
    }

    public void failJob(JobDbEntity jobDbEntity) {
        jobDbEntity.setStatus(JobStatus.FAILED);
        jobDbEntity.setCurrentProgress(-1);
        jobDbEntity.setLastUpdatedAt(now());
        this.jobDbRepository.save(jobDbEntity);
    }

    public Timestamp now() {
        return new Timestamp(System.currentTimeMillis());
    }

    public JobDbEntity getJobById(UUID jobId) throws SafaError {
        Optional<JobDbEntity> jobOption = this.jobDbRepository.findById(jobId);
        if (jobOption.isPresent()) {
            return jobOption.get();
        }
        throw new SafaError("Could not find job with id:" + jobId);
    }

    @PostConstruct
    public void init() {
        instance = this;
    }
}
