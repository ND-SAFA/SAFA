package edu.nd.crc.safa.features.generation.tgen;

import java.util.List;

import edu.nd.crc.safa.features.generation.common.GenerationLink;
import edu.nd.crc.safa.features.generation.common.ITGenResponse;

import lombok.Data;

/**
 * Output of predicting trace links.
 */
@Data
public class TGenResponse implements ITGenResponse {
    /**
     * List of links with their predicted similarity score.
     */
    private List<GenerationLink> predictions;
    private List<String> logs;
}
