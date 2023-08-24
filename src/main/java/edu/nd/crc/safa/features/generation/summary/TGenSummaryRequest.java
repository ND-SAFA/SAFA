package edu.nd.crc.safa.features.generation.summary;

import java.util.List;

import edu.nd.crc.safa.features.generation.common.GenerationArtifact;

import lombok.AllArgsConstructor;
import lombok.Data;

/**
 * The request to TGEN to summarize artifacts (or content).
 */
@Data
@AllArgsConstructor
public class TGenSummaryRequest {
    /**
     * The artifacts to summarize.
     */
    List<GenerationArtifact> artifacts;
    /**
     * The project summary.
     */
    String projectSummary = null;

    public TGenSummaryRequest(List<GenerationArtifact> artifacts) {
        this.artifacts = artifacts;
    }
}
