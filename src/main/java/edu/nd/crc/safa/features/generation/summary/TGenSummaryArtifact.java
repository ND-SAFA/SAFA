package edu.nd.crc.safa.features.generation.summary;

import javax.annotation.Nullable;
import javax.validation.constraints.NotNull;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * The artifact representation for summarization.
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
public class TGenSummaryArtifact {
    /**
     * The identifier of the artifact.
     */
    @Nullable
    String id;
    /**
     * Optional. Name of artifact to calculate type from.
     */
    @NotNull
    String name;
    /**
     * The content to summarize.
     */
    String content;
    /**
     * The type of summarization.
     */
    TGenSummaryArtifactType type = TGenSummaryArtifactType.NL;
}
