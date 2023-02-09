package edu.nd.crc.safa.features.models.tgen.entities.api;

import java.util.List;
import java.util.Map;

import lombok.Data;
import lombok.EqualsAndHashCode;

/**
 * Output of TGEN /predict/ endpoint.
 */
@Data
@EqualsAndHashCode(callSuper = true)
public class TGenPredictionOutput extends AbstractTGenResponse {
    /**
     * List of links with their predicted similarity score.
     */
    List<PredictedLink> predictions;
    /**
     * Metrics on predictions.
     */
    Map<String, Double> metrics;
    /**
     * Error message if status is 1.
     */
    String exception;

    /**
     * A predicted similarity score between a source and targe artifact.
     */
    @Data
    public static class PredictedLink {
        String source;
        String target;
        double score;
    }
}
