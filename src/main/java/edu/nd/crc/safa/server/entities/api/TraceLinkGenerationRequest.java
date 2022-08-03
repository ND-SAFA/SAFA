package edu.nd.crc.safa.server.entities.api;

import java.util.List;

import edu.nd.crc.safa.server.entities.app.project.ArtifactAppEntity;

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
