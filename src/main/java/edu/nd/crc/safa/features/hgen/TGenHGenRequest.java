package edu.nd.crc.safa.features.hgen;

import java.util.List;
import javax.validation.constraints.NotNull;

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
    @NotNull
    List<TGenSummaryArtifact> artifacts;
    /**
     * The type of artifacts to generate.
     */
    List<String> targetTypes;
}
