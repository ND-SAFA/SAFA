package edu.nd.crc.safa.features.generation.tgen.entities;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@NoArgsConstructor
@AllArgsConstructor
@Data
public class ArtifactLevelRequest {
    /**
     * The artifact type of the source artifacts.
     */
    private String source;
    /**
     * The artifact type of target artifacts.
     */
    private String target;
}
