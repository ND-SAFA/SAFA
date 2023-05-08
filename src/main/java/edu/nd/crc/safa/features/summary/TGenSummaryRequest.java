package edu.nd.crc.safa.features.summary;

import java.util.Map;

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
    Map<String, TGenSummaryArtifact> artifacts;
    /**
     * The LLM to use. Either GPT or Anthropic
     */
    String model;
}
