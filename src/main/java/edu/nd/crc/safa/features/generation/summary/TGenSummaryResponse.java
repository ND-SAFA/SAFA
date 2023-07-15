package edu.nd.crc.safa.features.generation.summary;

import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.features.generation.common.ITGenResponse;

import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * The response from the TGEN summarization endpoint.
 */
@Data
@NoArgsConstructor
public class TGenSummaryResponse implements ITGenResponse {
    /**
     * The content sent to summarize.
     */
    Map<String, TGenSummaryArtifact> artifacts;
    List<String> logs;
}
