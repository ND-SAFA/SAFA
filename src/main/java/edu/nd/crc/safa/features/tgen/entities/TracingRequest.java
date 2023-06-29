package edu.nd.crc.safa.features.tgen.entities;

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
    List<ArtifactLevelRequest> artifactLevels;
}
