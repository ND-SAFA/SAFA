package edu.nd.crc.safa.features.generation.api;

import java.util.List;
import java.util.stream.Collectors;

import edu.nd.crc.safa.config.TGenConfig;
import edu.nd.crc.safa.features.generation.common.GenerationDataset;
import edu.nd.crc.safa.features.generation.common.GenerationLink;
import edu.nd.crc.safa.features.generation.tgen.TGenRequest;
import edu.nd.crc.safa.features.generation.tgen.TGenResponse;
import edu.nd.crc.safa.features.jobs.logging.JobLogger;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@AllArgsConstructor
@Service
public class GenerateLinksApi {
    private final GenApiController genApiController;

    /**
     * Generates links using a deep learning model starting at a given state.
     *
     * @param dataset The dataset to trace.
     * @param logger  The logger used to send TGEN logs to.
     * @return List of generated traces.
     */
    public List<TraceAppEntity> generateLinks(
        GenerationDataset dataset, JobLogger logger) {
        // Step - Build request
        TGenRequest payload = new TGenRequest(dataset);

        // Step - Send request
        TGenResponse output = this.sendTraceLinkRequest(payload, logger);
        return convertPredictionsToLinks(output.getPredictions());
    }

    /**
     * Generates links through TGEN.
     *
     * @param payload The payload to send TGEN.
     * @param logger  The logger used to store trace link logs.
     * @return TGEN's response.
     */
    private TGenResponse sendTraceLinkRequest(TGenRequest payload, JobLogger logger) {
        String predictEndpoint;
        int candidates = payload.getDataset().getNumOfCandidates();
        genApiController.log(logger, String.format("Number of candidates: %s", candidates));
        predictEndpoint = TGenConfig.getEndpoint("tgen");
        return genApiController.performJob(predictEndpoint, payload, TGenResponse.class, logger);
    }

    /**
     * Converts trace link predictions to actual trace links.
     *
     * @param predictions TGEN link predictions.
     * @return The trace link entities.
     */
    private List<TraceAppEntity> convertPredictionsToLinks(
        List<GenerationLink> predictions) {
        return predictions
            .stream()
            .map(p ->
                new TraceAppEntity(
                    p.getSource(),
                    p.getTarget())
                    .asGeneratedTrace(p.getScore())
                    .withExplanation(p.getExplanation()))
            .collect(Collectors.toList());
    }
}
