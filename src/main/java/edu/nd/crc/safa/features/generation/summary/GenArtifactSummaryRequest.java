package edu.nd.crc.safa.features.generation.summary;

import java.util.List;
import javax.annotation.Nullable;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.features.generation.common.GenerationArtifact;

import lombok.AllArgsConstructor;
import lombok.Data;

/**
 * The request to TGEN to summarize artifacts (or content).
 */
@Data
@AllArgsConstructor
public class GenArtifactSummaryRequest {
    /**
     * The artifacts to summarize.
     */
    @NotEmpty
    List<@NotNull GenerationArtifact> artifacts;
    /**
     * The project summary.
     */
    @Nullable
    String projectSummary = null;

    public GenArtifactSummaryRequest(List<GenerationArtifact> artifacts) {
        this.artifacts = artifacts;
    }
}
