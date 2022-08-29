package edu.nd.crc.safa.features.tgen.entities;

import java.util.List;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;

import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Request to generate trace links between artifacts.
 */
@Data
@NoArgsConstructor
public class ArtifactTraceGenerationRequestDTO {
    /**
     * List of source artifacts.
     */
    List<ArtifactAppEntity> sourceArtifacts;
    /**
     * List of target artifacts
     */
    List<ArtifactAppEntity> targetArtifacts;
}
