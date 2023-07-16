package edu.nd.crc.safa.features.generation;

import java.util.List;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;

import edu.nd.crc.safa.config.TGenConfig;
import edu.nd.crc.safa.features.common.SafaRequestBuilder;
import edu.nd.crc.safa.features.generation.common.ITGenResponse;
import edu.nd.crc.safa.features.generation.common.TGenDataset;
import edu.nd.crc.safa.features.generation.common.TGenLink;
import edu.nd.crc.safa.features.generation.common.TGenStatus;
import edu.nd.crc.safa.features.generation.common.TGenTask;
import edu.nd.crc.safa.features.generation.hgen.HGenResponse;
import edu.nd.crc.safa.features.generation.hgen.TGenHGenRequest;
import edu.nd.crc.safa.features.generation.projectSummary.ProjectSummaryRequest;
import edu.nd.crc.safa.features.generation.projectSummary.ProjectSummaryResponse;
import edu.nd.crc.safa.features.generation.prompt.TGenPromptRequest;
import edu.nd.crc.safa.features.generation.prompt.TGenPromptResponse;
import edu.nd.crc.safa.features.generation.summary.TGenSummaryRequest;
import edu.nd.crc.safa.features.generation.summary.TGenSummaryResponse;
import edu.nd.crc.safa.features.generation.tgen.TGenPredictionRequestDTO;
import edu.nd.crc.safa.features.generation.tgen.TGenTraceGenerationResponse;
import edu.nd.crc.safa.features.jobs.logging.JobLogger;
import edu.nd.crc.safa.features.jobs.logging.entities.JobLogEntry;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.traces.ITraceGenerationController;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;

import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.NoArgsConstructor;
import org.javatuples.Pair;

/**
 * Responsible for providing an API for predicting trace links via TGEN.
 */
@AllArgsConstructor
public class GenerationApi implements ITraceGenerationController {

    private final SafaRequestBuilder safaRequestBuilder;

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
     * Generates project summary.
     *
     * @param request The request containing project artifacts.
     * @param logger  The job logger.
     * @return The project summary.
     */
    public String generateProjectSummary(ProjectSummaryRequest request, JobLogger logger) {
        String endpoint = getEndpoint("project-summary");
        ProjectSummaryResponse response = performTGenJob(endpoint, request, ProjectSummaryResponse.class, logger);
        return response.getSummary();
    }

    /**
     * Creates hierarchy of artifacts for artifacts.
     * TODO: Add logger.
     *
     * @param request The request detailing clusters of artifacts.
     * @return The generated artifacts per cluster.
     */
    public HGenResponse generateHierarchy(TGenHGenRequest request) {
        String summarizeEndpoint = getEndpoint("hgen");
        return this.performTGenJob(summarizeEndpoint, request, HGenResponse.class, null);
    }

    /**
     * Generates summaries for given content.
     *
     * @param request Contains content to summarize and associated parameters.
     * @param logger  Optional logger for relaying log messages.
     * @return TGen response.
     */
    public TGenSummaryResponse generateSummaries(TGenSummaryRequest request, JobLogger logger) {
        return sendSummarizeRequest(request, logger);
    }

    public TGenSummaryResponse sendSummarizeRequest(TGenSummaryRequest payload, JobLogger logger) {
        String predictEndpoint;

        int nArtifacts = payload.getArtifacts().size();
        log(logger, String.format("Summarizing %s artifacts.", nArtifacts));
        if (nArtifacts <= Defaults.SUMMARY_ARTIFACT_THRESHOLD) {
            predictEndpoint = getEndpoint("summarize-sync");
            return this.safaRequestBuilder.sendPost(predictEndpoint, payload, TGenSummaryResponse.class);
        } else {
            predictEndpoint = getEndpoint("summarize");
            return this.performTGenJob(predictEndpoint, payload, TGenSummaryResponse.class, logger);
        }
    }

    /**
     * Performs a completion request to TGen.
     * TODO: Add logger.
     *
     * @param request The request containing prompt.
     * @return The completion string.
     */
    public TGenPromptResponse generatePrompt(TGenPromptRequest request) {
        String generatePromptEndpoint = getEndpoint("complete");
        return this.performTGenJob(generatePromptEndpoint, request, TGenPromptResponse.class, null);
    }

    /**
     * Generates links using a deep learning model starting at a given state.
     *
     * @param dataset The dataset to trace.
     * @param logger  The logger used to send TGEN logs to.
     * @return List of generated traces.
     */
    public List<TraceAppEntity> generateLinks(
        TGenDataset dataset, JobLogger logger) {
        // Step - Build request
        TGenPredictionRequestDTO payload = new TGenPredictionRequestDTO(dataset);

        // Step - Send request
        TGenTraceGenerationResponse output = this.sendTraceLinkRequest(payload, logger);
        return convertPredictionsToLinks(output.getPredictions());
    }

    /**
     * Generates links through TGEN.
     *
     * @param payload The payload to send TGEN.
     * @param logger  The logger used to store trace link logs.
     * @return TGEN's response.
     */
    public TGenTraceGenerationResponse sendTraceLinkRequest(TGenPredictionRequestDTO payload, JobLogger logger) {
        String predictEndpoint;
        int candidates = payload.getDataset().getNumOfCandidates();
        log(logger, String.format("Number of candidates: %s", candidates));
        if (candidates <= Defaults.TRACE_CANDIDATE_THRESHOLD) {
            predictEndpoint = getEndpoint("predict-sync");
            return this.safaRequestBuilder.sendPost(predictEndpoint, payload, TGenTraceGenerationResponse.class);
        } else {
            predictEndpoint = getEndpoint("predict");
            return this.performTGenJob(predictEndpoint, payload, TGenTraceGenerationResponse.class, logger);
        }
    }

    public TGenTraceGenerationResponse performSearch(TGenPredictionRequestDTO payload, JobLogger logger) {
        int candidates = payload.getDataset().getNumOfCandidates();
        log(logger, String.format("Number of candidates: %s", candidates));
        String predictEndpoint = getEndpoint("predict-sync");
        return this.safaRequestBuilder.sendPost(predictEndpoint, payload, TGenTraceGenerationResponse.class);
    }

    /**
     * Submits job to TGen and polls status until job is completed or has failed.
     *
     * @param endpoint      The endpoint to send payload to.
     * @param payload       The job to submit to TGEN.
     * @param responseClass The class for the job result.
     * @param <T>           The generic for the job result class.
     * @return Parsed TGEN response if job is successful.
     */
    private <T extends ITGenResponse> T performTGenJob(String endpoint,
                                                       Object payload,
                                                       Class<T> responseClass,
                                                       JobLogger logger) {
        TGenTask task = this.safaRequestBuilder.sendPost(endpoint, payload, TGenTask.class);
        String statusEndpoint = getEndpoint("status");
        String resultEndpoint = getEndpoint("results");
        boolean jobFinshed = false;
        TGenStatus tGenStatus = null;
        int currentLogIndex = 0;
        JobLogEntry jobEntry = null;
        Pair<Integer, JobLogEntry> logResponse;
        while (!jobFinshed) {
            tGenStatus = this.safaRequestBuilder.sendPost(statusEndpoint, task, TGenStatus.class);
            List<String> logs = tGenStatus.getLogs();
            logResponse = writeLogs(logger, logs, currentLogIndex, jobEntry);
            currentLogIndex = logResponse.getValue0();
            jobEntry = logResponse.getValue1();
            if (tGenStatus.getStatus() <= 0) { // TODO : Update to use enum
                jobFinshed = true;
            } else {
                sleep(Defaults.WAIT_SECONDS);
            }
        }

        if (tGenStatus.getStatus() == 0) {
            T response = this.safaRequestBuilder.sendPost(resultEndpoint, task, responseClass);
            logResponse = writeLogs(logger, response.getLogs(), currentLogIndex, jobEntry);
            currentLogIndex = logResponse.getValue0();
            jobEntry = logResponse.getValue1();
            return response;
        }
        throw new SafaError(tGenStatus.getMessage());
    }

    /**
     * Converts trace link predictions to actual trace links.
     *
     * @param predictions TGEN link predictions.
     * @return The trace link entities.
     */
    private List<TraceAppEntity> convertPredictionsToLinks(
        List<TGenLink> predictions) {
        return predictions
            .stream()
            .map(p -> new TraceAppEntity(
                p.getSource(),
                p.getTarget()
            ).asGeneratedTrace(p.getScore())).collect(Collectors.toList());
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
     * Returns TGEN endpoint path.
     *
     * @param endpointName The name of the endpoint.
     * @return Endpoint path according to current environment.
     */
    private String getEndpoint(String endpointName) {
        return TGenConfig.get().getTGenEndpoint(endpointName);
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
     * Contains default values for magic constants.
     */
    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    static class Defaults {
        static final int WAIT_SECONDS = 5;
        static final int TRACE_CANDIDATE_THRESHOLD = 50;
        static final int SUMMARY_ARTIFACT_THRESHOLD = 50;
    }
}
