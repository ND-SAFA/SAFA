package edu.nd.crc.safa.server.services;

import java.sql.Timestamp;
import java.util.List;
import javax.annotation.PostConstruct;

import edu.nd.crc.safa.server.authentication.SafaUserService;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.api.jobs.JobType;
import edu.nd.crc.safa.server.entities.app.JobStatus;
import edu.nd.crc.safa.server.entities.db.Job;
import edu.nd.crc.safa.server.entities.db.SafaUser;
import edu.nd.crc.safa.server.repositories.JobRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
 * Responsible for creating units-of-work to be used in JobController.
 */
@Service
public class JobService {

    private static JobService instance;
    JobRepository jobRepository;
    SafaUserService safaUserService;

    @Autowired
    public JobService(JobRepository jobRepository, SafaUserService safaUserService) {
        this.jobRepository = jobRepository;
        this.safaUserService = safaUserService;
    }

    public static JobService getInstance() {
        return instance;
    }

    public List<Job> retrieveCurrentUserJobs() throws SafaError {
        SafaUser currentUser = this.safaUserService.getCurrentUser();
        return this.jobRepository.findByUser(currentUser);
    }

    public Job createNewJob(JobType jobType) {
        SafaUser currentUser = this.safaUserService.getCurrentUser();
        Job job = new Job(
            currentUser,
            jobType,
            JobStatus.IN_PROGRESS,
            now(),
            now(),
            null,
            0,
            0
        );
        this.jobRepository.save(job);
        return job;
    }

    public void startStep(Job job) {
        job.setLastUpdatedAt(now());
        this.jobRepository.save(job);
    }

    public void endStep(Job job) {
        job.incrementStep();
        job.setLastUpdatedAt(now());
        this.jobRepository.save(job);
    }

    public void completeJob(Job job) {
        job.setStatus(JobStatus.COMPLETED);
        job.setCurrentProgress(100);
        job.setCompletedAt(now());
        job.setLastUpdatedAt(now());
        this.jobRepository.save(job);
    }

    public void failJob(Job job) {
        job.setStatus(JobStatus.FAILED);
        job.setCurrentProgress(-1);
        job.setLastUpdatedAt(now());
        this.jobRepository.save(job);
    }

    public Timestamp now() {
        return new Timestamp(System.currentTimeMillis());
    }

    @PostConstruct
    public void init() {
        instance = this;
    }
}
