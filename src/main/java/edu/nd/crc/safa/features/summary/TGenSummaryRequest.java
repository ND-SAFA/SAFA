package edu.nd.crc.safa.features.summary;

import java.util.List;

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
    List<TGenSummaryArtifact> artifacts;
}
