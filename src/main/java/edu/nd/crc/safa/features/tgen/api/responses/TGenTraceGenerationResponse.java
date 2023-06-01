package edu.nd.crc.safa.features.tgen.api.responses;

import java.util.List;

import lombok.Data;
import lombok.EqualsAndHashCode;

/**
 * Output of predicting trace links.
 */
@Data
@EqualsAndHashCode(callSuper = true)
public class TGenTraceGenerationResponse extends AbstractTGenResponse {
    /**
     * List of links with their predicted similarity score.
     */
    List<PredictedLink> predictions;

    /**
     * A predicted similarity score between a source and targe artifact.
     */
    @Data
    public static class PredictedLink {
        String source;
        String target;
        double score;
        double label = -1;
    }
}
