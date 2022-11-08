package edu.nd.crc.safa.features.models.tgen.method.bert;

import java.io.IOException;
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
import edu.nd.crc.safa.features.models.entities.api.TGenTrainingRequest;
import edu.nd.crc.safa.features.models.tgen.entities.ArtifactLevel;
import edu.nd.crc.safa.features.models.tgen.entities.ITraceLinkGeneration;
import edu.nd.crc.safa.features.models.tgen.entities.TracingPayload;
import edu.nd.crc.safa.features.models.tgen.entities.TracingRequest;
import edu.nd.crc.safa.features.models.tgen.entities.api.AbstractTGenResponse;
import edu.nd.crc.safa.features.models.tgen.entities.api.TGenJobResponseDTO;
import edu.nd.crc.safa.features.models.tgen.entities.api.TGenPredictionOutput;
import edu.nd.crc.safa.features.models.tgen.entities.api.TGenPredictionRequestDTO;
import edu.nd.crc.safa.features.models.tgen.entities.api.TGenTrainingResponse;
import edu.nd.crc.safa.features.models.tgen.generator.TraceGenerationService;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.traces.entities.db.ApprovalStatus;
import edu.nd.crc.safa.features.traces.entities.db.TraceType;
import edu.nd.crc.safa.utilities.CloudStorage;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.cloud.storage.Blob;
import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import org.json.JSONObject;

/**
 * Responsible for providing an API for predicting trace links using TBert.
 */
public abstract class TBert implements ITraceLinkGeneration {

    private final SafaRequestBuilder safaRequestBuilder;
    private final ObjectMapper mapper = new ObjectMapper();

    protected TBert(SafaRequestBuilder safaRequestBuilder) {
        this.safaRequestBuilder = safaRequestBuilder;
    }

    /**
     * Copies model defined by given subclass and saves it in new output path.
     *
     * @param newModelPath The path to save the new model to.
     */
    public void createModel(String newModelPath) {
        BertMethodIdentifier methodId = this.getBertMethodIdentifier();
        copyModel(methodId.getStatePath(), newModelPath);
    }

    /**
     * Copies model state in source path to target path.
     *
     * @param sourceStatePath The path to the state of the model to copy.
     * @param targetStatePath The path to store the new model at.
     */
    public void copyModel(String sourceStatePath, String targetStatePath) {
        BertMethodIdentifier methodId = this.getBertMethodIdentifier();
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
        BertMethodIdentifier methodId = this.getBertMethodIdentifier();
        ModelIdentifierDTO creationRequest = new ModelIdentifierDTO();
        creationRequest.setModelPath(methodId.getStatePath());
        this.safaRequestBuilder
            .sendPost(TBertConfig.get().getDeleteModelEndpoint(),
                creationRequest,
                ModelIdentifierDTO.class);
    }

    @Override
    public List<TraceAppEntity> generateLinksWithBaselineState(TracingPayload tracingPayload) {
        return this.generateLinksWithState(this.getBertMethodIdentifier().getStatePath(), false, tracingPayload);
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
        boolean loadFromStorage,
        TracingPayload tracingPayload) {
        // Step - Build request
        TGenPredictionRequestDTO payload = createTraceGenerationPayload(
            statePath,
            loadFromStorage,
            tracingPayload);

        // Step - Send request
        String predictEndpoint = TBertConfig.get().getPredictEndpoint();
        TGenJobResponseDTO response = this.safaRequestBuilder
            .sendPost(predictEndpoint, payload, TGenJobResponseDTO.class);

        if (response.getJobID() == null) {
            throw new SafaError("Received null output path from TGEN.");
        }

        // Step - Convert to response
        String outputPath = response.getJobID();
        TGenPredictionOutput output = getOutput(outputPath, TGenPredictionOutput.class);
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
        // Step - Build request
        TGenTrainingRequest trainingPayload = createTrainingPayload(statePath, tracingRequests, projectAppEntity);

        // Step - Send request
        String trainEndpoint = TBertConfig.get().getTrainEndpoint();
        TGenJobResponseDTO response = this.safaRequestBuilder
            .sendPost(trainEndpoint, trainingPayload, TGenJobResponseDTO.class);

        // Step - Convert to response
        getOutput(response.getJobID(), TGenTrainingResponse.class);
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
        boolean loadFromStorage,
        TracingPayload tracingPayload) {
        BertMethodIdentifier methodId = this.getBertMethodIdentifier();
        return new TGenPredictionRequestDTO(
            methodId.getBaseModel(),
            statePath,
            loadFromStorage,
            createArtifactPayload(tracingPayload, ArtifactLevel::getSources),
            createArtifactPayload(tracingPayload, ArtifactLevel::getTargets),
            new HashMap<>());
    }

    private TGenTrainingRequest createTrainingPayload(String statePath,
                                                      TracingRequest tracingRequest,
                                                      ProjectAppEntity projectAppEntity) {
        BertMethodIdentifier methodId = this.getBertMethodIdentifier();
        TracingPayload tracingPayload = TraceGenerationService.extractPayload(tracingRequest, projectAppEntity);
        return new TGenTrainingRequest(
            methodId.getBaseModel(),
            statePath,
            createArtifactPayload(tracingPayload, ArtifactLevel::getSources),
            createArtifactPayload(tracingPayload, ArtifactLevel::getTargets),
            projectAppEntity.getTraces());
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

    private <T extends AbstractTGenResponse> T getOutput(String jobId, Class<T> responseClass) {
        //TODO: Use scheduled tasks instead of constant pinging.
        String outputFile = CloudStorage.getJobOutputPath(jobId);
        try {
            while (!CloudStorage.exists(outputFile)) {
                Thread.sleep(1000 * Defaults.WAIT_SECONDS);
            }
            Blob blob = CloudStorage.getBlob(outputFile);
            JSONObject json = CloudStorage.downloadJsonFileBlob(blob);

            System.out.println("File Json:" + json);

            if (json.getInt("status") == -1) {
                throw new SafaError("TBert failed while generating links: " + json.getString("exception"));
            }
            T predictionOutput = mapper.readValue(json.toString(), responseClass);
            System.out.println("Prediction output:" + predictionOutput);
            if (predictionOutput.getStatus() == -1) {
                throw new SafaError(predictionOutput.getException());
            }
            return predictionOutput;
        } catch (InterruptedException e) {
            e.printStackTrace();
            throw new SafaError("Interrupted while waiting for output of generated links.");
        } catch (IOException e) {
            e.printStackTrace();
            throw new SafaError("IOException occurred while reading output of generated links.");
        } catch (Exception e) {
            e.printStackTrace();
            throw new SafaError("An error occurred while training the model", e);
        }
    }

    abstract BertMethodIdentifier getBertMethodIdentifier();

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    static class Defaults {
        static final int WAIT_SECONDS = 5;
    }
}
