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
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.hgen.TGenHGenRequest;
import edu.nd.crc.safa.features.hgen.TGenHGenResponse;
import edu.nd.crc.safa.features.jobs.logging.JobLogger;
import edu.nd.crc.safa.features.models.tgen.entities.ITraceGenerationController;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.prompt.TGenPromptRequest;
import edu.nd.crc.safa.features.prompt.TGenPromptResponse;
import edu.nd.crc.safa.features.summary.TGenSummaryRequest;
import edu.nd.crc.safa.features.summary.TGenSummaryResponse;
import edu.nd.crc.safa.features.tgen.api.AbstractTGenResponse;
import edu.nd.crc.safa.features.tgen.api.TGenDataset;
import edu.nd.crc.safa.features.tgen.api.TGenPredictionOutput;
import edu.nd.crc.safa.features.tgen.api.TGenPredictionRequestDTO;
import edu.nd.crc.safa.features.tgen.entities.ArtifactLevel;
import edu.nd.crc.safa.features.tgen.entities.TGenStatus;
import edu.nd.crc.safa.features.tgen.entities.TGenTask;
import edu.nd.crc.safa.features.tgen.entities.TracingPayload;
import edu.nd.crc.safa.features.tgen.method.BertMethodIdentifier;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.ApprovalStatus;
import edu.nd.crc.safa.features.traces.entities.db.TraceType;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;

/**
 * Responsible for providing an API for predicting trace links via TGEN.
 */
public class TGen implements ITraceGenerationController {

    public static JobLogger logger;

    private final SafaRequestBuilder safaRequestBuilder;
    private final BertMethodIdentifier methodId;

    public TGen(BertMethodIdentifier methodId) {
        this.safaRequestBuilder = ServiceProvider.instance.getSafaRequestBuilder();
        this.methodId = methodId;
    }

    /**
     * Creates hierarchy of artifacts for artifacts.
     *
     * @param request The request detailing clusters of artifacts.
     * @return The generated artifacts per cluster.
     */
    public TGenHGenResponse generateHierarchy(TGenHGenRequest request) {
        String summarizeEndpoint = getEndpoint("hgen");
        return this.requestTGen(summarizeEndpoint, request, TGenHGenResponse.class);
    }

    /**
     * Generates summaries for given content.
     *
     * @param request Contains content to summarize and assocatied parameteres.
     * @return TGen response.
     */
    public TGenSummaryResponse generateSummaries(TGenSummaryRequest request) {
        String summarizeEndpoint = getEndpoint("summarize");
        return this.requestTGen(summarizeEndpoint, request, TGenSummaryResponse.class);
    }

    /**
     * Performs a completion request to TGen.
     *
     * @param request The request containing prompt.
     * @return The completion string.
     */
    public TGenPromptResponse generatePrompt(TGenPromptRequest request) {
        String generatePromptEndpoint = getEndpoint("complete");
        return this.requestTGen(generatePromptEndpoint, request, TGenPromptResponse.class);
    }

    public TGenPredictionOutput performPrediction(TGenPredictionRequestDTO payload) {
        String predictEndpoint = TGenConfig.get().getTGenEndpoint("predict");
        return this.requestTGen(predictEndpoint, payload, TGenPredictionOutput.class);
    }

    /**
     * Generates trace link predictions for each pair of source and target artifacts.
     *
     * @param tracingPayload Levels of artifacts defining sources and targets.
     * @return List of generated trace links.
     */
    public List<TraceAppEntity> generateLinksWithBaselineState(TracingPayload tracingPayload) {
        return this.generateLinksWithState(methodId.getStatePath(), tracingPayload);
    }

    public List<TraceAppEntity> generateLinksWithState(
        String statePath,
        TracingPayload tracingPayload) {
        // Step - Build request
        TGenPredictionRequestDTO payload = createTraceGenerationPayload(
            statePath,
            tracingPayload);

        // Step - Send request
        TGenPredictionOutput output = this.performPrediction(payload);
        return convertPredictionsToLinks(output.getPredictions());
    }


    private List<TraceAppEntity> convertPredictionsToLinks(List<TGenPredictionOutput.PredictedLink> predictions) {
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

    private TGenPredictionRequestDTO createTraceGenerationPayload(
        String statePath,
        TracingPayload tracingPayload) {
        TGenDataset dataset = new TGenDataset(
            createArtifactPayload(tracingPayload, ArtifactLevel::getSources),
            createArtifactPayload(tracingPayload, ArtifactLevel::getTargets));
        return new TGenPredictionRequestDTO(statePath, dataset);
    }

    private List<Map<String, String>> createArtifactPayload(TracingPayload tracingPayload, Function<ArtifactLevel,
        List<ArtifactAppEntity>> getter) {
        List<Map<String, String>> artifactLevelsMap = new ArrayList<>();

        tracingPayload.getArtifactLevels().stream().map(getter).forEach(artifacts -> {
            Map<String, String> artifactLevelsArtifactMap = new HashMap<>();
            artifacts.forEach(a -> artifactLevelsArtifactMap.put(a.getName(), a.getTraceString()));
            artifactLevelsMap.add(artifactLevelsArtifactMap);
        });
        return artifactLevelsMap;
    }

    private <T extends AbstractTGenResponse> T requestTGen(String endpoint, Object payload, Class<T> responseClass) {
        TGenTask task = this.safaRequestBuilder.sendPost(endpoint, payload, TGenTask.class);
        String statusEndpoint = getEndpoint("status");
        String resultEndpoint = getEndpoint("results");
        boolean jobFinshed = false;
        TGenStatus tGenStatus = null;
        while (tGenStatus == null || !jobFinshed) {
            tGenStatus = this.safaRequestBuilder.sendPost(statusEndpoint, task, TGenStatus.class);
            if (tGenStatus.getStatus() <= 0) { // TODO : Update to use enum
                jobFinshed = true;
            } else {
                sleep(Defaults.WAIT_SECONDS);
            }
        }

        if (tGenStatus.getStatus() == 0) {
            T response = this.safaRequestBuilder.sendPost(resultEndpoint, task, responseClass);
            if (logger != null) {
                logger.log(response.getLog());
            }
            return response;
        }
        throw new SafaError(tGenStatus.getMessage());
    }

    public String getEndpoint(String endpointName) {
        return TGenConfig.get().getTGenEndpoint(endpointName);
    }

    public void sleep(int secondsToSleep) {
        try {
            TimeUnit.SECONDS.sleep(secondsToSleep);
        } catch (InterruptedException ie) {
            Thread.currentThread().interrupt();
        }
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    static class Defaults {
        static final int WAIT_SECONDS = 1;
    }
}
