package edu.nd.crc.safa.features.generation.summary;

import java.util.List;

import edu.nd.crc.safa.features.generation.common.GenerationArtifact;

import jakarta.annotation.Nullable;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;

/**
 * The request to TGEN to summarize artifacts (or content).
 */
@Data
@AllArgsConstructor
public class SummaryRequest {
    /**
     * The artifacts to summarize.
     */
    @NotEmpty
    private List<@NotNull GenerationArtifact> artifacts;
    /**
     * The project summary.
     */
    @Nullable
    private String projectSummary = null;

    public SummaryRequest(List<GenerationArtifact> artifacts) {
        this.artifacts = artifacts;
    }
}
