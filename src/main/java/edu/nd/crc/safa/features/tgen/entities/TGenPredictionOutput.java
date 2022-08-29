package edu.nd.crc.safa.features.tgen.entities;

import java.util.List;
import java.util.Map;

import lombok.Data;

/**
 * Output of TGEN /predict/ endpoint.
 */
@Data
public class TGenPredictionOutput {
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
     * 0 = success, 1 = failed.
     */
    int status;

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
