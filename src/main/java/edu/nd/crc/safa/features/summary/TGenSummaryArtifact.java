package edu.nd.crc.safa.features.summary;

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
     * The content to summarize.
     */
    String content;
    /**
     * The type of summarization.
     */
    TGenSummaryArtifactType type = TGenSummaryArtifactType.NL;
}
