package edu.nd.crc.safa.features.summary;

import java.util.List;

import edu.nd.crc.safa.features.tgen.api.requests.AbstractGenerationRequest;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * A request to summarize artifacts from the front-end.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class SummarizeRequestDTO extends AbstractGenerationRequest {
    /**
     * The artifacts to summarize and their type.
     */
    List<TGenSummaryArtifact> artifacts;
}
