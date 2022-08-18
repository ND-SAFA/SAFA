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
public class TraceLinkGenerationRequest {

    List<ArtifactAppEntity> sourceArtifacts;
    List<ArtifactAppEntity> targetArtifacts;
}
