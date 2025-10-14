package edu.nd.crc.safa.features.generation.hgen;

import java.util.List;

import edu.nd.crc.safa.features.generation.common.GenerationArtifact;

import jakarta.validation.constraints.NotNull;
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
    private List<GenerationArtifact> artifacts;
    /**
     * The type of artifacts to generate.
     */
    private List<String> targetTypes;
    /**
     * The project summary.
     */
    private String summary;
}
