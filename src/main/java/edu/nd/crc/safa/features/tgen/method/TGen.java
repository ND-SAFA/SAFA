package edu.nd.crc.safa.features.tgen.method;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;

import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.config.TGenConfig;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.common.SafaRequestBuilder;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.hgen.TGenHGenRequest;
import edu.nd.crc.safa.features.hgen.TGenHGenResponse;
import edu.nd.crc.safa.features.models.tgen.entities.ITraceGenerationController;
import edu.nd.crc.safa.features.prompt.TGenPromptRequest;
import edu.nd.crc.safa.features.prompt.TGenPromptResponse;
import edu.nd.crc.safa.features.summary.TGenSummaryRequest;
import edu.nd.crc.safa.features.summary.TGenSummaryResponse;
import edu.nd.crc.safa.features.tgen.api.TGenDataset;
import edu.nd.crc.safa.features.tgen.api.TGenPredictionOutput;
import edu.nd.crc.safa.features.tgen.api.TGenPredictionRequestDTO;
import edu.nd.crc.safa.features.tgen.entities.ArtifactLevel;
import edu.nd.crc.safa.features.tgen.entities.TracingPayload;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.ApprovalStatus;
import edu.nd.crc.safa.features.traces.entities.db.TraceType;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Responsible for providing an API for predicting trace links via TGEN.
 */
public class TGen implements ITraceGenerationController {

    private static final Logger log = LoggerFactory.getLogger(TGen.class);

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
        String summarizeEndpoint = TGenConfig.get().getHGenEndpoint();
        return this.safaRequestBuilder.sendPost(summarizeEndpoint, request, TGenHGenResponse.class);
    }

    /**
     * Generates summaries for given content.
     *
     * @param request Contains content to summarize and assocatied parameteres.
     * @return TGen response.
     */
    public TGenSummaryResponse generateSummaries(TGenSummaryRequest request) {
        String summarizeEndpoint = TGenConfig.get().getSummarizeEndpoint();
        return this.safaRequestBuilder.sendPost(summarizeEndpoint, request, TGenSummaryResponse.class);
    }

    /**
     * Performs a completion request to TGen.
     *
     * @param request The request containing prompt.
     * @return The completion string.
     */
    public TGenPromptResponse generatePrompt(TGenPromptRequest request) {
        String generatePromptEndpoint = TGenConfig.get().getPromptCompletionEndpoint();
        return this.safaRequestBuilder.sendPost(generatePromptEndpoint, request, TGenPromptResponse.class);
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

    public TGenPredictionOutput performPrediction(TGenPredictionRequestDTO payload) {
        String predictEndpoint = TGenConfig.get().getPredictEndpoint();
        return this.safaRequestBuilder
            .sendPost(predictEndpoint, payload, TGenPredictionOutput.class);
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
            artifacts.forEach(a -> {
                String summary = a.getSummary();
                if (summary != null && summary.length() > 0) {
                    artifactLevelsArtifactMap.put(a.getName(), summary);
                } else {
                    artifactLevelsArtifactMap.put(a.getName(), a.getBody());
                }
            });
            artifactLevelsMap.add(artifactLevelsArtifactMap);
        });
        return artifactLevelsMap;
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    static class Defaults {
        static final int WAIT_SECONDS = 5;
    }
}
