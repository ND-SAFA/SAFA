package edu.nd.crc.safa.features.generation.api;

import java.util.List;
import java.util.concurrent.TimeUnit;

import edu.nd.crc.safa.config.TGenConfig;
import edu.nd.crc.safa.features.common.RequestService;
import edu.nd.crc.safa.features.generation.common.ITGenResponse;
import edu.nd.crc.safa.features.generation.common.TGenStatus;
import edu.nd.crc.safa.features.generation.common.TGenTask;
import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;
import edu.nd.crc.safa.features.jobs.logging.JobLogger;
import edu.nd.crc.safa.features.jobs.logging.entities.JobLogEntry;
import edu.nd.crc.safa.features.jobs.repositories.JobDbRepository;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;

import lombok.AllArgsConstructor;
import org.javatuples.Pair;
import org.springframework.stereotype.Service;

@AllArgsConstructor
@Service
public class ApiController {
    private static final int WAIT_SECONDS = 5;
    private static final int HOURS = 3600;
    private static final int MAX_DURATION = 4 * HOURS; // 4 hours
    private final RequestService requestService;
    private final JobDbRepository jobDbRepository;

    /**
     * Submits job to TGen and polls status until job is completed or has failed.
     *
     * @param endpoint      The endpoint to send payload to.
     * @param payload       The job to submit to TGEN.
     * @param responseClass The class for the job result.
     * @param <T>           The generic for the job result class.
     * @return Parsed TGEN response if job is successful.
     */
    public <T extends ITGenResponse> T performJob(String endpoint,
                                                  Object payload,
                                                  Class<T> responseClass,
                                                  JobLogger logger) {
        String statusEndpoint = TGenConfig.getEndpoint("status");
        String resultEndpoint = TGenConfig.getEndpoint("results");

        long startTime = System.currentTimeMillis();
        long endTime;

        boolean jobFinshed = false;
        TGenStatus tGenStatus = null;
        int currentLogIndex = 0;
        JobLogEntry jobEntry = null;
        Pair<Integer, JobLogEntry> logResponse;
        String error = "No current error.";
        int retries = 0;
        int maxRetries = 3;

        // Create task
        TGenTask task = this.requestService.sendPost(endpoint, payload, TGenTask.class);
        if (logger != null) {
            JobDbEntity job = logger.getJob();
            job.setTaskId(task.getTaskId());
            this.jobDbRepository.save(job);
        }


        while (!jobFinshed) {
            try {
                endTime = System.currentTimeMillis();
                long duration = (endTime - startTime) / 1000; // Duration in seconds
                if (duration >= MAX_DURATION) {
                    jobFinshed = true;
                    error = String.format("Worker has reached the maximum allowed duration of %s seconds.",
                        MAX_DURATION);
                }
                tGenStatus = this.requestService.sendPost(statusEndpoint, task, TGenStatus.class);
                List<String> logs = tGenStatus.getLogs();
                logResponse = writeLogs(logger, logs, currentLogIndex, jobEntry);
                currentLogIndex = logResponse.getValue0();
                jobEntry = logResponse.getValue1();
            } catch (Exception e) {
                retries++;
                if (retries >= maxRetries) {
                    log(logger, e.getMessage());
                    error = "This job has reached the maximum number of retries.";
                    log(logger, error);
                    throw new SafaError(error);
                } else {
                    log(logger, e.getMessage());
                    log(logger, "Status call for job failed, retrying...");
                    sleep(WAIT_SECONDS);
                }
            }

            if (tGenStatus == null) {
                throw new SafaError("Received null status from job.");
            } else if (tGenStatus.getStatus().hasFailed()) {
                jobFinshed = true;
                error = tGenStatus.getMessage();
            } else if (tGenStatus.getStatus().hasSucceeded()) {
                T response = this.requestService.sendPost(resultEndpoint, task, responseClass);
                logResponse = writeLogs(logger, response.getLogs(), currentLogIndex, jobEntry);
                if (logger != null) {
                    JobDbEntity job = logger.getJob();
                    job.setTaskId(null);
                    this.jobDbRepository.save(job);
                }
                return response;
            } else {
                sleep(WAIT_SECONDS);
            }
        }
        throw new SafaError(error);
    }

    /**
     * Writes the latest logs to the job logger.
     *
     * @param logs            List of logs incoming from TGEN.
     * @param currentLogIndex The index of the current log to write.
     * @param jobLog          The job entry to log under.
     * @return The new current log index and the updated job log.
     */
    private Pair<Integer, JobLogEntry> writeLogs(JobLogger logger,
                                                 List<String> logs,
                                                 int currentLogIndex,
                                                 JobLogEntry jobLog) {
        if (currentLogIndex >= logs.size()) {
            return new Pair<>(currentLogIndex, jobLog);
        }
        String currentLog = String.join("\n", logs.subList(currentLogIndex, logs.size()));
        if (currentLog.length() > 0) {
            if (jobLog == null) {
                jobLog = log(logger, currentLog);
            } else {
                jobLog = logger.addToLog(jobLog, currentLog);
            }

            return new Pair(logs.size(), jobLog);
        }
        return new Pair(currentLogIndex, jobLog);
    }

    /**
     * Sleeps the current thread.
     *
     * @param secondsToSleep The number of seconds to sleep.
     */
    private void sleep(int secondsToSleep) {
        try {
            TimeUnit.SECONDS.sleep(secondsToSleep);
        } catch (InterruptedException ie) {
            Thread.currentThread().interrupt();
        }
    }

    /**
     * Logs message to current job.
     *
     * @param message The message to log.
     * @return The updated job entry associated with logger.
     */
    protected JobLogEntry log(JobLogger logger, String message) {
        if (logger != null) {
            return logger.log(message);
        }
        return null;
    }
}
