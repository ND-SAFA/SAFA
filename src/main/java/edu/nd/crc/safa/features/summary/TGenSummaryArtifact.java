package edu.nd.crc.safa.features.summary;

import lombok.Data;

/**
 * The artifact representation for summarization.
 */
@Data
class TGenSummaryArtifact {
    /**
     * The content to summarize.
     */
    String content;
    /**
     * The type of summarization.
     */
    TGenSummaryArtifactType type = TGenSummaryArtifactType.NL;
}
