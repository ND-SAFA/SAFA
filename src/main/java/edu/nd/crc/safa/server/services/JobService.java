package edu.nd.crc.safa.server.services;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.db.Job;
import edu.nd.crc.safa.server.repositories.JobRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
 * Responsible for creating units-of-work to be used in JobController.
 */
@Service
public class JobService {

    JobRepository jobRepository;

    @Autowired
    public JobService(JobRepository jobRepository) {
        this.jobRepository = jobRepository;
    }

    public Job retrieveJob(UUID jobId) throws SafaError {
        Optional<Job> jobOptional = this.jobRepository.findById(jobId);

        if (jobOptional.isPresent()) {
            return jobOptional.get();
        }
        throw new SafaError("No job exist with id:" + jobId);
    }
}
