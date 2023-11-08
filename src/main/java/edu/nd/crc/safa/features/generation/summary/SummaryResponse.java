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
@NoArgsConstructor
@Data
public class SummaryResponse implements ITGenResponse {
    /**
     * The content sent to summarize.
     */
    private List<GenerationArtifact> artifacts;
    /**
     * The project summary used in context to summarize artifacts.
     */
    private String summary;
    /**
     * The logs associated with job.
     */
    private List<String> logs;
}
