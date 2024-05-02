package edu.nd.crc.safa.features.health;

import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.features.generation.common.GenerationArtifact;

import lombok.Data;

@Data
public class HealthGenResponse {
    /**
     * List of direct matches with concept artifacts.
     */
    private List<ConceptMatchDTO> matches;
    /**
     * Map of location matched to the multiple concepts matched at that location.
     */
    private Map<Integer, List<ConceptMatchDTO>> multiMatches;
    /**
     * List of traces predicted between concept and artifact.
     */
    private List<GenerationArtifact> predictedMatches;
    /**
     * List of entities found in artifact but missing in concept artifacts.
     */
    private List<String> undefinedEntities;
}
