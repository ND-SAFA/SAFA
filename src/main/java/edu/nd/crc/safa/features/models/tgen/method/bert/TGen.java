package edu.nd.crc.safa.features.models.tgen.method.bert;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;

import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.config.TBertConfig;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.common.SafaRequestBuilder;
import edu.nd.crc.safa.features.models.entities.api.ModelIdentifierDTO;
import edu.nd.crc.safa.features.models.tgen.entities.ArtifactLevel;
import edu.nd.crc.safa.features.models.tgen.entities.ITraceLinkGeneration;
import edu.nd.crc.safa.features.models.tgen.entities.TracingPayload;
import edu.nd.crc.safa.features.models.tgen.entities.TracingRequest;
import edu.nd.crc.safa.features.models.tgen.entities.api.TGenDataset;
import edu.nd.crc.safa.features.models.tgen.entities.api.TGenPredictionOutput;
import edu.nd.crc.safa.features.models.tgen.entities.api.TGenPredictionRequestDTO;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.ApprovalStatus;
import edu.nd.crc.safa.features.traces.entities.db.TraceType;

import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import org.apache.commons.lang3.NotImplementedException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Responsible for providing an API for predicting trace links via TGEN.
 */
public class TGen implements ITraceLinkGeneration {

    private static final Logger log = LoggerFactory.getLogger(TGen.class);

    private final SafaRequestBuilder safaRequestBuilder;
    private final ObjectMapper mapper = new ObjectMapper();
    private final BertMethodIdentifier methodId;

    public TGen(SafaRequestBuilder safaRequestBuilder, BertMethodIdentifier methodId) {
        this.safaRequestBuilder = safaRequestBuilder;
        this.methodId = methodId;
    }

    /**
     * Copies model defined by given subclass and saves it in new output path.
     *
     * @param newModelPath The path to save the new model to.
     */
    public void createModel(String newModelPath) {
        copyModel(methodId.getStatePath(), newModelPath);
    }

    /**
     * Copies model state in source path to target path.
     *
     * @param sourceStatePath The path to the state of the model to copy.
     * @param targetStatePath The path to store the new model at.
     */
    public void copyModel(String sourceStatePath, String targetStatePath) {
        ModelIdentifierDTO creationRequest = new ModelIdentifierDTO(
            methodId.getBaseModel(),
            sourceStatePath,
            targetStatePath
        );
        this.safaRequestBuilder
            .sendPost(TBertConfig.get().getCreateModelEndpoint(),
                creationRequest,
                ModelIdentifierDTO.class);
    }

    /**
     * Deletes model by sending request to TGEN to delete model files
     */
    public void deleteModel() {
        ModelIdentifierDTO creationRequest = new ModelIdentifierDTO();
        creationRequest.setModelPath(methodId.getStatePath());
        this.safaRequestBuilder
            .sendPost(TBertConfig.get().getDeleteModelEndpoint(),
                creationRequest,
                ModelIdentifierDTO.class);
    }

    @Override
    public List<TraceAppEntity> generateLinksWithBaselineState(TracingPayload tracingPayload) {
        return this.generateLinksWithState(methodId.getStatePath(), tracingPayload);
    }

    /**
     * Generates trace link predictions for each pair of source and target artifacts.
     *
     * @param statePath      The path to the initial model state.
     * @param tracingPayload Levels of artifacts defining sources and targets.
     * @return List of generated trace links.
     */
    @Override
    public List<TraceAppEntity> generateLinksWithState(
        String statePath,
        TracingPayload tracingPayload) {
        // Step - Build request
        TGenPredictionRequestDTO payload = createTraceGenerationPayload(
            statePath,
            tracingPayload);

        // Step - Send request
        String predictEndpoint = TBertConfig.get().getPredictEndpoint();
        TGenPredictionOutput output = this.safaRequestBuilder
            .sendPost(predictEndpoint, payload, TGenPredictionOutput.class);
        return convertPredictionsToLinks(output.getPredictions());
    }

    /**
     * Trains model defined by subclass to predict the given trace links.
     * Trace links not present in `traces` are assumed to be non-links (score = 0).
     *
     * @param statePath        Path to starting weights of model.
     * @param tracingRequests  Levels of artifacts defining sources and targets.
     * @param projectAppEntity The project to extract the artifacts from.
     */
    public void trainModel(String statePath,
                           TracingRequest tracingRequests,
                           ProjectAppEntity projectAppEntity) {
        throw new NotImplementedException("Training a model is deprecated. Please use a default model instead.");
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
            artifacts.forEach(a -> artifactLevelsArtifactMap.put(a.getName(), a.getBody()));
            artifactLevelsMap.add(artifactLevelsArtifactMap);
        });
        return artifactLevelsMap;
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    static class Defaults {
        static final int WAIT_SECONDS = 5;
    }
}
