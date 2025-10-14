package edu.nd.crc.safa.features.health.entities.gen;

import java.util.List;
import java.util.Map;

import edu.nd.crc.safa.features.generation.common.GenerationLink;
import edu.nd.crc.safa.features.health.entities.ConceptMatchDTO;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;
import lombok.Data;

@Data
@JsonIgnoreProperties(ignoreUnknown = true)
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public class GenHealthResponse {
    /**
     * List of Artifact IDs that experience a contradiction with target artifact.
     */
    private List<GenContradiction> contradictions;
    /**
     * List of entities found in artifact but missing in concept artifacts.
     */
    private List<GenUndefinedEntity> undefinedConcepts;
    /**
     * List of direct matches with concept artifacts.
     */
    private List<ConceptMatchDTO> directMatches;
    /**
     * Map of location matched to the multiple concepts matched at that location.
     */
    private Map<String, Map<Integer, List<ConceptMatchDTO>>> multiMatches;
    /**
     * List of traces predicted between concept and artifact.
     */
    private List<GenerationLink> predictedMatches;
}
