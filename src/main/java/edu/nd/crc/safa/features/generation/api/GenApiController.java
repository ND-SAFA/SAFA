package edu.nd.crc.safa.features.generation.api;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.TimeUnit;

import edu.nd.crc.safa.config.TGenConfig;
import edu.nd.crc.safa.features.common.RequestService;
import edu.nd.crc.safa.features.generation.common.TGenStatus;
import edu.nd.crc.safa.features.generation.common.TGenTask;
import edu.nd.crc.safa.features.jobs.logging.JobLogger;
import edu.nd.crc.safa.features.jobs.logging.entities.JobLogEntry;
import edu.nd.crc.safa.features.jobs.services.JobService;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@AllArgsConstructor
@Service
public class GenApiController {
    private static final String GEN_COOKIE_KEY = "GEN_KEY";
    private static final int WAIT_SECONDS = 2;
    private static final int HOURS = 3600;
    private static final int MAX_DURATION = 6 * HOURS; // 6 hours
    private final RequestService requestService;
    private JobService jobService;

    /**
     * Submits job to TGen and polls status until job is completed or has failed.
     *
     * @param endpoint      The endpoint to send payload to.
     * @param payload       The job to submit to TGEN.
     * @param responseClass The class for the job result.
     * @param <T>           The generic for the job result class.
     * @param logger        The logger to store logs under.
     * @return Parsed TGEN response if job is successful.
     */
    public <T> T performJob(String endpoint,
                            Object payload,
                            Class<T> responseClass,
                            JobLogger logger) {
        TGenTask<T> task = performRequest(endpoint, payload, TGenTask.class);
        task.setResponseClass(responseClass);
        setTaskId(logger, task.getTaskId());
        T result = pollTGenTask(task, t -> writeLogs(logger, t), MAX_DURATION, WAIT_SECONDS);
        setTaskId(logger, null);
        return result;
    }

    /**
     * Sends authenticated request to GEN api.
     *
     * @param endpoint      The GEN endpoint.
     * @param payload       The payload to endpoint.
     * @param responseClass The response class to serialize output into.
     * @param <T>           Type of response class.
     * @return Serialized data.
     */
    public <T> T performRequest(String endpoint,
                                Object payload,
                                Class<T> responseClass) {
        // Step - Send request
        Map<String, String> cookies = new HashMap<>();
        cookies.put(GEN_COOKIE_KEY, TGenConfig.get().getGenKey());
        return this.requestService.sendPost(endpoint, payload, cookies, responseClass);
    }

    /**
     * Polls the task status until complete. Throws error if failure occurs to job or while getting status.
     *
     * @param task     The task to wait until its completion.
     * @param timeout  The maximum amount of seconds to wait for task to complete.
     * @param waitTime The time to wait between status requests.
     * @param <T>      The class of the response of the task.
     * @return The job result.
     */
    private <T> T pollTGenTask(TGenTask<T> task, TaskHandler taskHandler, long timeout, int waitTime) {
        pollWithTimeout(() -> {
            updateTaskStatus(task);
            taskHandler.handleTask(task);
            TGenStatus status = task.getStatus();
            if (status.getStatus().hasFailed()) {
                String message = status.getMessage();
                message = message == null ? "Unknown GEN error occurred. Likely OOM." : message;
                throw new SafaError(message);
            }
            return status.getStatus().hasCompleted();
        }, timeout, waitTime);
        return getJobResult(task, task.getResponseClass());
    }

    /**
     * Gets the result of the task.
     *
     * @param task          The task that has been completed.
     * @param responseClass The class of the task result.
     * @param <T>           The type of class of the task result.
     * @return The response of the job.
     */
    private <T> T getJobResult(TGenTask<T> task, Class<T> responseClass) {
        String resultEndpoint = TGenConfig.getEndpoint("results");
        return this.performRequest(resultEndpoint, task, responseClass);
    }

    /**
     * Repeatedly calls task handler until is successfully exits. Throws error if handler exceeds the timeout time.
     *
     * @param statusHandler Callable to check on the job status.
     * @param timeout       The number of seconds before timeout error is thrown.
     * @param waitTime      The number of seconds to wait between status calls.
     */
    private void pollWithTimeout(StatusHandler statusHandler, long timeout, int waitTime) {
        long startTime = System.currentTimeMillis();
        long endTime;

        boolean result;
        do {
            result = statusHandler.statusHandler();
            endTime = System.currentTimeMillis();
            long duration = (endTime - startTime) / 1000; // Duration in seconds
            if (duration >= timeout) {
                String error = String.format("Worker has reached the maximum allowed duration of %s seconds.",
                    MAX_DURATION);
                throw new SafaError(error);
            }
            sleep(waitTime);
        } while (!result);
    }

    /**
     * Returns whether job has finished.
     *
     * @param task The task associated with job to check.
     */
    private void updateTaskStatus(TGenTask task) {
        String statusEndpoint = TGenConfig.getEndpoint("status");
        TGenStatus tGenStatus = this.performRequest(statusEndpoint, task, TGenStatus.class);

        if (tGenStatus.getStatus().hasFailed()) {
            throw new SafaError(tGenStatus.getMessage());
        }
        task.updateStatus(tGenStatus);
    }

    /**
     * Writes the latest logs in the task status to the logger.
     */
    private void writeLogs(JobLogger logger, TGenTask task) {
        TGenStatus status = task.getStatus();
        if (status == null) {
            return;
        }
        List<String> logs = status.getLogs();
        int currentLogIndex = status.getCurrentLogIndex();

        if (currentLogIndex >= logs.size()) {
            return;
        }
        String currentLog = String.join("\n", logs.subList(currentLogIndex, logs.size()));
        if (currentLog.length() > 0) {
            JobLogEntry jobLog = status.getJobLogEntry();
            jobLog = jobLog == null ? log(logger, currentLog) : logger.addToLog(jobLog, currentLog);
            status.setJobLogEntry(jobLog);
            currentLogIndex = logs.size();
            status.setCurrentLogIndex(currentLogIndex);
        }
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

    /**
     * Sets the current task on job associated with logger.
     *
     * @param logger The logger potentially containing job.
     * @param taskID The ID of the task to associated with job.
     */
    private void setTaskId(JobLogger logger, UUID taskID) {
        if (logger != null) {
            this.jobService.setJobTask(logger.getJob(), taskID);
        }
    }

}
