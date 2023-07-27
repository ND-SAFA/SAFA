package edu.nd.crc.safa.features.generation.tgen;

import java.util.List;

import edu.nd.crc.safa.features.generation.common.GenerationLink;
import edu.nd.crc.safa.features.generation.common.ITGenResponse;

import lombok.Data;

/**
 * Output of predicting trace links.
 */
@Data
public class TGenTraceGenerationResponse implements ITGenResponse {
    /**
     * List of links with their predicted similarity score.
     */
    List<GenerationLink> predictions;
    List<String> logs;
}
