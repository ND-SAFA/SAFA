package edu.nd.crc.safa.features.summary;

import java.util.Map;

import edu.nd.crc.safa.features.tgen.api.AbstractTGenResponse;

import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * The response from the TGEN summarization endpoint.
 */
@Data
@NoArgsConstructor
public class TGenSummaryResponse extends AbstractTGenResponse {
    /**
     * The content sent to summarize.
     */
    Map<String, TGenSummaryArtifact> artifacts;
}
