package edu.nd.crc.safa.features.health;

import java.util.List;

import edu.nd.crc.safa.features.generation.common.GenerationArtifact;

import lombok.AllArgsConstructor;
import lombok.Data;

@AllArgsConstructor
@Data
public class HealthGenRequest {
    /**
     * List of artifacts in project.
     */
    private List<GenerationArtifact> projectArtifacts;
    /**
     * Target artifact to generate health checks for.
     */
    private GenerationArtifact targetArtifacts;
}
