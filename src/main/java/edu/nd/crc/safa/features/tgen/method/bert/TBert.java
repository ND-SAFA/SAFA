package edu.nd.crc.safa.features.tgen.method.bert;

import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import edu.nd.crc.safa.common.SafaRequestBuilder;
import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.config.TBertConfig;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.models.entities.api.ModelCreationRequest;
import edu.nd.crc.safa.features.models.entities.api.TGenTrainingRequest;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.tgen.entities.ITraceLinkGeneration;
import edu.nd.crc.safa.features.tgen.entities.api.AbstractTGenResponse;
import edu.nd.crc.safa.features.tgen.entities.api.TGenJobResponseDTO;
import edu.nd.crc.safa.features.tgen.entities.api.TGenPredictionOutput;
import edu.nd.crc.safa.features.tgen.entities.api.TGenPredictionRequestDTO;
import edu.nd.crc.safa.features.tgen.entities.api.TGenTrainingResponse;
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
     * @param outputPath The path to save the new model to.
     */
    public void createModel(String outputPath) {
        BertMethodIdentifier methodId = this.getBertMethodIdentifier();
        ModelCreationRequest creationRequest = new ModelCreationRequest(
            methodId.getBaseModel(),
            methodId.getModelPath(),
            outputPath
        );
        this.safaRequestBuilder
            .sendPost(TBertConfig.get().getCreateModelEndpoint(),
                creationRequest,
                ModelCreationRequest.class);
    }

    @Override
    public List<TraceAppEntity> generateLinksWithBaselineState(
        List<ArtifactAppEntity> sources,
        List<ArtifactAppEntity> targets) {
        return this.generateLinksWithState(this.getBertMethodIdentifier().getModelPath(),
            false,
            sources,
            targets);
    }

    /**
     * Generates trace link predictions for each pair of source and target artifacts.
     *
     * @param statePath The path to the initial model state.
     * @param sources   The source artifacts.
     * @param targets   The target artifacts.
     * @return List of generated trace links.
     */
    @Override
    public List<TraceAppEntity> generateLinksWithState(
        String statePath,
        boolean loadFromStorage,
        List<ArtifactAppEntity> sources,
        List<ArtifactAppEntity> targets) {
        // Step - Build request
        TGenPredictionRequestDTO payload = createTraceGenerationPayload(
            statePath,
            loadFromStorage,
            sources,
            targets);

        // Step - Send request
        String predictEndpoint = TBertConfig.get().getPredictEndpoint();
        TGenJobResponseDTO response = this.safaRequestBuilder
            .sendPost(predictEndpoint, payload, TGenJobResponseDTO.class);
        System.out.println("Response:" + response);

        // Step - Convert to response
        String outputPath = response.getOutputPath();
        System.out.println("OutputPath: " + outputPath);
        TGenPredictionOutput output = getOutput(outputPath, TGenPredictionOutput.class);
        return convertPredictionsToLinks(output.getPredictions());
    }

    /**
     * Trains model defined by subclass to predict the given trace links.
     * Trace links not present in `traces` are assumed to be non-links (score = 0).
     *
     * @param statePath Path to starting weights of model.
     * @param sources   The source artifacts.
     * @param targets   The target artifacts.
     * @param traces    The traces between source and target artifacts.
     */
    public void trainModel(String statePath,
                           List<ArtifactAppEntity> sources,
                           List<ArtifactAppEntity> targets,
                           List<TraceAppEntity> traces) {
        // Step - Build request
        TGenTrainingRequest trainingPayload = createTrainingPayload(statePath, sources, targets, traces);

        // Step - Send request
        String trainEndpoint = TBertConfig.get().getTrainEndpoint();
        TGenJobResponseDTO response = this.safaRequestBuilder
            .sendPost(trainEndpoint, trainingPayload, TGenJobResponseDTO.class);
        System.out.println("Response: " + response);

        // Step - Convert to response
        getOutput(response.getOutputPath(), TGenTrainingResponse.class);
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
        List<ArtifactAppEntity> sources,
        List<ArtifactAppEntity> targets) {
        BertMethodIdentifier methodId = this.getBertMethodIdentifier();
        return new TGenPredictionRequestDTO(
            methodId.getBaseModel(),
            statePath,
            loadFromStorage,
            createArtifactPayload(sources),
            createArtifactPayload(targets));
    }

    private TGenTrainingRequest createTrainingPayload(String statePath,
                                                      List<ArtifactAppEntity> sources,
                                                      List<ArtifactAppEntity> targets,
                                                      List<TraceAppEntity> traces) {
        BertMethodIdentifier methodId = this.getBertMethodIdentifier();
        return new TGenTrainingRequest(
            methodId.getBaseModel(),
            statePath,
            createArtifactPayload(sources),
            createArtifactPayload(targets),
            traces);
    }

    private Map<String, String> createArtifactPayload(List<ArtifactAppEntity> artifacts) {
        Map<String, String> artifactMap = new HashMap<>();
        artifacts.forEach(a -> artifactMap.put(a.getName(), a.getBody()));
        return artifactMap;
    }

    private <T extends AbstractTGenResponse> T getOutput(String outputFile, Class<T> responseClass) {
        //TODO: Use scheduled tasks instead of constant pinging.
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
        } finally {
            if (CloudStorage.exists(outputFile)) {
                CloudStorage.getBlob(outputFile).delete();
            }
        }
    }

    abstract BertMethodIdentifier getBertMethodIdentifier();

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    static class Defaults {
        static final int WAIT_SECONDS = 5;
    }
}
