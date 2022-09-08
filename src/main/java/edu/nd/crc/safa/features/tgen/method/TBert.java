package edu.nd.crc.safa.features.tgen.method;

import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import edu.nd.crc.safa.common.SafaRequestBuilder;
import edu.nd.crc.safa.config.ProjectVariables;
import edu.nd.crc.safa.config.TBertConfig;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.tgen.entities.ITraceLinkGeneration;
import edu.nd.crc.safa.features.tgen.entities.TGenJobResponseDTO;
import edu.nd.crc.safa.features.tgen.entities.TGenPredictionOutput;
import edu.nd.crc.safa.features.tgen.entities.TGenPredictionRequestDTO;
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
public class TBert implements ITraceLinkGeneration {

    private final SafaRequestBuilder safaRequestBuilder;
    private final ObjectMapper mapper = new ObjectMapper();

    public TBert(SafaRequestBuilder safaRequestBuilder) {
        this.safaRequestBuilder = safaRequestBuilder;
    }

    public List<TraceAppEntity> generateLinks(List<ArtifactAppEntity> sources, List<ArtifactAppEntity> targets) {
        // Step - Build request
        TGenPredictionRequestDTO predictionRequest = new TGenPredictionRequestDTO(
            Defaults.TBERT_BASE_MODEL,
            Defaults.TBERT_PATH,
            createArtifactPayload(sources),
            createArtifactPayload(targets));

        // Step - Send request
        String predictEndpoint = TBertConfig.get().getPredictEndpoint();
        TGenJobResponseDTO response = this.safaRequestBuilder
            .sendPost(predictEndpoint, predictionRequest, TGenJobResponseDTO.class);

        // Step - Convert to response
        TGenPredictionOutput output = getOutput(response.getOutputPath());
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

    private Map<String, String> createArtifactPayload(List<ArtifactAppEntity> artifacts) {
        Map<String, String> artifactMap = new HashMap<>();
        artifacts.forEach(a -> artifactMap.put(a.getName(), a.getBody()));
        return artifactMap;
    }

    private TGenPredictionOutput getOutput(String outputFile) {
        //TODO: Use scheduled tasks instead of constant pinging.
        try {
            while (!CloudStorage.exists(outputFile)) {
                Thread.sleep(1000 * Defaults.WAIT_SECONDS);
            }
            Blob blob = CloudStorage.getBlob(outputFile);
            JSONObject json = CloudStorage.downloadJsonFileBlob(blob);

            if (json.getInt("status") == -1) {
                throw new SafaError("TBert failed while generating links: " + json.getString("exception"));
            }
            TGenPredictionOutput predictionOutput = mapper.readValue(json.toString(), TGenPredictionOutput.class);
            return predictionOutput;
        } catch (InterruptedException e) {
            throw new SafaError("Interrupted while waiting for output of generated links.");
        } catch (IOException e) {
            throw new SafaError("IOException occurred while reading output of generated links.");
        } finally {
            if (CloudStorage.exists(outputFile)) {
                CloudStorage.getBlob(outputFile).delete();
            }
        }
    }

    @NoArgsConstructor(access = AccessLevel.PRIVATE)
    static class Defaults {
        static final int WAIT_SECONDS = 5;
        static final String TBERT_BASE_MODEL = "bert_trace_single";
        static final String TBERT_PATH = "thearod5/tbert";
    }
}
