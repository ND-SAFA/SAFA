package edu.nd.crc.safa.features.generation.summary;

import java.util.List;

import edu.nd.crc.safa.features.generation.common.GenerationArtifact;
import edu.nd.crc.safa.features.generation.common.ITGenResponse;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * The response from the TGEN summarization endpoint.
 */
@JsonIgnoreProperties(ignoreUnknown = true)
@Data
@NoArgsConstructor
public class TGenSummaryResponse implements ITGenResponse {
    /**
     * The content sent to summarize.
     */
    List<GenerationArtifact> artifacts;
    String summary;
    List<String> logs;
}
