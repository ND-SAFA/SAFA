package edu.nd.crc.safa.features.tgen.entities;

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
    String source;
    /**
     * The artifact type of target artifacts.
     */
    String target;
}
