package edu.nd.crc.safa.features.generation.tgen.entities;

import java.util.List;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@NoArgsConstructor
@AllArgsConstructor
@Data
public class TracingRequest {
    /**
     * List of artifact levels to trace.
     */
    private List<ArtifactLevelRequest> artifactLevels;
    /**
     * The tracing algorithm to use.
     */
    private TGenAlgorithms method = TGenAlgorithms.GENERATION;
}
