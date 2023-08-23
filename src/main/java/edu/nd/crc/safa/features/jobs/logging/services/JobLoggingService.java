package edu.nd.crc.safa.features.jobs.logging.services;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.jobs.entities.app.JobSteps;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.jobs.logging.entities.JobLogEntry;
import edu.nd.crc.safa.features.jobs.logging.entities.JobLogEntryAppEntity;
import edu.nd.crc.safa.features.jobs.logging.repositories.JobLogEntryRepository;
import edu.nd.crc.safa.features.jobs.services.JobService;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.app.SafaItemNotFoundError;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.users.services.PermissionCheckerService;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class JobLoggingService {

    private JobLogEntryRepository jobLogEntryRepository;

    private JobService jobService;

    private PermissionCheckerService permissionCheckerService;

    /**
     * Get all logs for a job step. This does not check if the step number is valid
     * or if the job exists, and will just return an empty list in those cases.
     *
     * @param job The job the step is a part of.
     * @param stepNum The index of the step.
     * @return A list of logs sorted by timestamp.
     */
    public List<JobLogEntry> getLogsForJobStep(JobDbEntity job, short stepNum) {
        return jobLogEntryRepository.findByJobAndStepNumOrderByTimestampAsc(job, stepNum);
    }

    /**
     * Get all logs for a job step. This does not check if the step number is valid,
     * but it will validate that the job exists and is accessible to the user.
     *
     * @param jobUuid The ID of the job the step is a part of.
     * @param user The user making the request.
     * @param stepNum The index of the step.
     * @return A list of logs sorted by timestamp.
     */
    public List<JobLogEntry> getLogsForJobStep(UUID jobUuid, SafaUser user, short stepNum) {
        return getLogsForJobStep(getJob(jobUuid, user), stepNum);
    }

    /**
     * Get all logs for a job step as entities that are convertible to json.
     * This does not check if the step number is valid or if the job exists,
     * and will just return an empty list in those cases.
     *
     * @param job The job the step is a part of.
     * @param stepNum The index of the step.
     * @return A list of logs sorted by timestamp.
     */
    public List<JobLogEntryAppEntity> getJsonLogEntitiesForJobStep(JobDbEntity job, short stepNum) {
        return getLogsForJobStep(job, stepNum).stream()
                .map(this::getJsonEntityFromDatabaseEntity)
                .collect(Collectors.toList());
    }

    /**
     * Get all logs for a job step as entities that are convertible to json.
     * This does not check if the step number is valid, but it will validate
     * that the job exists and is accessible to the user.
     *
     * @param jobUuid The ID of the job the step is a part of.
     * @param user The user making the request.
     * @param stepNum The index of the step.
     * @return A list of logs sorted by timestamp.
     */
    public List<JobLogEntryAppEntity> getJsonLogEntitiesForJobStep(UUID jobUuid, SafaUser user, short stepNum) {
        return getJsonLogEntitiesForJobStep(getJob(jobUuid, user), stepNum);
    }

    /**
     * Gets all logs associated with a job.
     *
     * @param job The job to get the logs of.
     * @return A list of [lists of logs sorted by timestamp] for each job step.
     */
    public List<List<JobLogEntry>> getLogsForJob(JobDbEntity job) {
        List<String> steps = JobSteps.getJobSteps(job.getJobType());

        List<List<JobLogEntry>> jobLogs = new ArrayList<>(steps.size());

        for (short stepNum = 0; stepNum < steps.size(); ++stepNum) {
            jobLogs.add(getLogsForJobStep(job, stepNum));
        }

        return jobLogs;
    }

    /**
     * Gets all logs associated with a job. This will validate that the job exists
     * and is accessible to the user.
     *
     * @param id The ID of the job to get the logs of.
     * @param user The user that is trying to access the logs.
     * @return A list of [lists of logs sorted by timestamp] for each job step.
     */
    public List<List<JobLogEntry>> getLogsForJob(UUID id, SafaUser user) {
        return getLogsForJob(getJob(id, user));
    }

    /**
     * Gets all logs associated with a job as entities that are convertible to json.
     *
     * @param job The job to get the logs of.
     * @return A list of [lists of logs sorted by timestamp] for each job step.
     */
    public List<List<JobLogEntryAppEntity>> getJsonLogEntitiesForJob(JobDbEntity job) {
        return getLogsForJob(job).stream()
                .map(List::stream)
                .map(stream -> stream.map(this::getJsonEntityFromDatabaseEntity))
                .map(stream -> stream.collect(Collectors.toList()))
                .collect(Collectors.toList());
    }

    /**
     * Gets all logs associated with a job as entities that are convertible to json.
     * This will validate that the job exists and is accessible to the user.
     *
     * @param id The ID of the job to get the logs of.
     * @param user The user that is trying to access the logs.
     * @return A list of [lists of logs sorted by timestamp] for each job step.
     */
    public List<List<JobLogEntryAppEntity>> getJsonLogEntitiesForJob(UUID id, SafaUser user) throws SafaError {
        return getJsonLogEntitiesForJob(getJob(id, user));
    }

    /**
     * Convert a job log database entity into an entity suitable for converting to json and
     * sending to the front end.
     *
     * @param entry The database job log entity.
     * @return The front end job log entity
     */
    public JobLogEntryAppEntity getJsonEntityFromDatabaseEntity(JobLogEntry entry) {
        return new JobLogEntryAppEntity(entry.getTimestamp(), entry.getEntry());
    }

    /**
     * Adds a log entry to the database.
     *
     * @param entry The entry to add.
     * @return The saved entity.
     */
    public JobLogEntry saveLog(JobLogEntry entry) {
        return jobLogEntryRepository.save(entry);
    }

    /**
     * Validates that a job with the given ID exists and is accessible by the
     * user, and then returns that job.
     *
     * @param id The ID of the job to retrieve.
     * @param user The user trying to access the job.
     * @return The job, if it exists and the user is allowed to see it.
     * @throws SafaItemNotFoundError If the job does not exist or the current user doesn't have access to it.
     */
    private JobDbEntity getJob(UUID id, SafaUser user) throws SafaItemNotFoundError {
        try {
            JobDbEntity job = jobService.getJobById(id);

            if (permissionCheckerService.hasViewPermission(job, user)) {
                return job;
            }

        } catch (SafaItemNotFoundError ignored) {
            // Fall through to error below to make the error message consistent
        }

        throw new SafaItemNotFoundError("Job with id %s does not exist or you do not have permission to view it.", id);
    }
}
