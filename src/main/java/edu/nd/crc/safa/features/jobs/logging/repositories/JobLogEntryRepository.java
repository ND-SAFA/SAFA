package edu.nd.crc.safa.features.jobs.logging.repositories;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.jobs.logging.entities.JobLogEntry;

import org.springframework.data.repository.CrudRepository;

public interface JobLogEntryRepository extends CrudRepository<JobLogEntry, UUID> {

    List<JobLogEntry> findByJobAndStepNumOrderByTimestampAsc(JobDbEntity job, short stepNum);

    List<JobLogEntry> findByJob(JobDbEntity job);
}
