package edu.nd.crc.safa.features.summary;

import java.util.Map;

import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * The response from the TGEN summarization endpoint.
 */
@Data
@NoArgsConstructor
public class TGenSummaryResponse {
    /**
     * The content sent to summarize.
     */
    Map<String, TGenSummaryArtifact> artifacts;
}
