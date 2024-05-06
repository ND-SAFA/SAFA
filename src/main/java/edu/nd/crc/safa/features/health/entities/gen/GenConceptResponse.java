package edu.nd.crc.safa.features.health.entities.gen;

import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.features.generation.common.GenerationArtifact;
import edu.nd.crc.safa.features.generation.common.GenerationLink;
import edu.nd.crc.safa.features.health.entities.ConceptMatchDTO;

import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;
import lombok.Data;

@Data
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public class GenConceptResponse {
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
    private List<GenerationLink> predictedMatches;
    /**
     * List of entities found in artifact but missing in concept artifacts.
     */
    private List<GenerationArtifact> undefinedEntities;
}
