package edu.nd.crc.safa.features.tgen;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeUnit;
import java.util.function.Function;
import java.util.stream.Collectors;

import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.config.TGenConfig;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.common.SafaRequestBuilder;
import edu.nd.crc.safa.features.hgen.TGenHGenRequest;
import edu.nd.crc.safa.features.hgen.TGenHGenResponse;
import edu.nd.crc.safa.features.jobs.logging.JobLogger;
import edu.nd.crc.safa.features.jobs.logging.entities.JobLogEntry;
import edu.nd.crc.safa.features.models.ITraceGenerationController;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.prompt.TGenPromptRequest;
import edu.nd.crc.safa.features.prompt.TGenPromptResponse;
import edu.nd.crc.safa.features.summary.TGenSummaryRequest;
import edu.nd.crc.safa.features.summary.TGenSummaryResponse;
import edu.nd.crc.safa.features.tgen.api.TGenDataset;
import edu.nd.crc.safa.features.tgen.api.requests.TGenPredictionRequestDTO;
import edu.nd.crc.safa.features.tgen.api.responses.AbstractTGenResponse;
import edu.nd.crc.safa.features.tgen.api.responses.TGenTraceGenerationResponse;
import edu.nd.crc.safa.features.tgen.entities.ArtifactLevel;
import edu.nd.crc.safa.features.tgen.entities.TGenStatus;
import edu.nd.crc.safa.features.tgen.entities.TGenTask;
import edu.nd.crc.safa.features.tgen.entities.TracingPayload;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.ApprovalStatus;
import edu.nd.crc.safa.features.traces.entities.db.TraceType;

import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.NoArgsConstructor;
import org.javatuples.Pair;

/**
 * Responsible for providing an API for predicting trace links via TGEN.
 */
@AllArgsConstructor
public class TGen implements ITraceGenerationController {

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
     * Creates hierarchy of artifacts for artifacts.
     * TODO: Add logger.
     *
     * @param request The request detailing clusters of artifacts.
     * @return The generated artifacts per cluster.
     */
    public TGenHGenResponse generateHierarchy(TGenHGenRequest request) {
        String summarizeEndpoint = getEndpoint("hgen");
        return this.performTGenJob(summarizeEndpoint, request, TGenHGenResponse.class, null);
    }

    /**
     * Generates summaries for given content.
     *
     * @param request Contains content to summarize and assocatied parameteres.
     * @return TGen response.
     */
    public TGenSummaryResponse generateSummaries(TGenSummaryRequest request) {
        String summarizeEndpoint = getEndpoint("summarize");
        return this.safaRequestBuilder.sendPost(summarizeEndpoint, request, TGenSummaryResponse.class);
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
     * @param tracingPayload The artifact to trace between.
     * @param logger         The logger used to send TGEN logs to.
     * @return List of generated traces.
     */
    public List<TraceAppEntity> generateLinks(
        TracingPayload tracingPayload, JobLogger logger) {
        // Step - Build request
        TGenPredictionRequestDTO payload = createTraceGenerationPayload(
            tracingPayload);

        // Step - Send request
        TGenTraceGenerationResponse output = this.sendTraceLinkRequest(payload, logger);
        return convertPredictionsToLinks(output.getPredictions());
    }

    /**
     * Generates links through TGEN.
     *
     * @param payload The payload to send TGEN.
     * @return TGEN's response.
     */
    public TGenTraceGenerationResponse sendTraceLinkRequest(TGenPredictionRequestDTO payload, JobLogger logger) {
        String predictEndpoint;
        int candidates = payload.getDataset().getNumOfCandidates();
        log(logger, String.format("Number of candidates: %s", candidates));
        if (candidates <= Defaults.CANDIDATE_THRESHOLD) {
            predictEndpoint = getEndpoint("predict-sync");
            return this.safaRequestBuilder.sendPost(predictEndpoint, payload, TGenTraceGenerationResponse.class);

        } else {
            predictEndpoint = getEndpoint("predict");
            return this.performTGenJob(predictEndpoint, payload, TGenTraceGenerationResponse.class, logger);
        }
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
    private <T extends AbstractTGenResponse> T performTGenJob(String endpoint,
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
        List<TGenTraceGenerationResponse.PredictedLink> predictions) {
        return predictions
            .stream()
            .filter(p -> p.getScore() > ProjectVariables.TRACE_THRESHOLD)
            .map(p -> new TraceAppEntity(
                null,
                p.getSource(),
                null,
                p.getTarget(),
                null,
                ApprovalStatus.UNREVIEWED,
                p.getScore(),
                TraceType.GENERATED
            )).collect(Collectors.toList());
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
     * Converts Client trace generation payload into TGEN payload.
     *
     * @param tracingPayload The tracing payload defined by client.
     * @return The payload to send TGEN.
     */
    private TGenPredictionRequestDTO createTraceGenerationPayload(
        TracingPayload tracingPayload) {
        TGenDataset dataset = new TGenDataset(
            createArtifactPayload(tracingPayload, ArtifactLevel::getSources),
            createArtifactPayload(tracingPayload, ArtifactLevel::getTargets));
        return new TGenPredictionRequestDTO(dataset, null);
    }

    /**
     * Creates the artifact payload based on the given TracingPayload and a getter function.
     *
     * @param tracingPayload The TracingPayload object containing the artifact levels.
     * @param getter         A function that retrieves a list of ArtifactAppEntity objects based on the ArtifactLevel.
     * @return A list of maps representing the artifact levels and their corresponding artifacts.
     */
    private List<Map<String, String>> createArtifactPayload(TracingPayload tracingPayload,
                                                            Function<ArtifactLevel, List<ArtifactAppEntity>> getter) {
        List<Map<String, String>> artifactLevelsMap = new ArrayList<>();

        tracingPayload.getArtifactLevels().stream().map(getter).forEach(artifacts -> {
            Map<String, String> artifactLevelsArtifactMap = new HashMap<>();
            artifacts
                .stream()
                .filter(a -> a.getTraceString().length() > 0)
                .forEach(a -> artifactLevelsArtifactMap.put(a.getName(), a.getTraceString()));
            artifactLevelsMap.add(artifactLevelsArtifactMap);
        });
        return artifactLevelsMap;
    }

    /**
     * Contains default values for magic constants.
     */
    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    static class Defaults {
        static final int WAIT_SECONDS = 5;
        static final int CANDIDATE_THRESHOLD = 50;
    }
}
