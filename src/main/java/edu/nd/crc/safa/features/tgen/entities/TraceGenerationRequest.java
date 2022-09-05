package edu.nd.crc.safa.features.tgen.entities;

import java.util.List;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;

import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Request to generate trace links between artifacts.
 */
@Data
@NoArgsConstructor
public class TraceGenerationRequest {
    /**
     * List of source artifacts.
     */
    @NotNull
    List<ArtifactAppEntity> sourceArtifacts;
    /**
     * List of target artifacts.
     */
    @NotNull
    List<ArtifactAppEntity> targetArtifacts;
    /**
     * The method to generate trace links with.
     */
    TraceGenerationMethod method = TraceGenerationMethod.VSM;
}
