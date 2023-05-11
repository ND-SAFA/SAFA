package edu.nd.crc.safa.features.hgen;

import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.features.summary.TGenSummaryArtifact;

import lombok.AllArgsConstructor;
import lombok.Data;

/**
 * The front-end request for hierarchy generation.
 */
@Data
@AllArgsConstructor
public class TGenHGenRequest {
    /**
     * The artifacts used in clusters.
     */
    Map<String, TGenSummaryArtifact> artifacts;
    /**
     * Describes the ids of artifacts in each cluster.
     */
    List<List<String>> clusters;
    /**
     * The model to use for HGEN.
     */
    String model;
}
