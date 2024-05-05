package edu.nd.crc.safa.features.health;

import java.util.List;

import edu.nd.crc.safa.features.generation.common.GenerationLink;

import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;
import lombok.Data;

@Data
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public class HealthGenResponse {
    /**
     * List of concept matches.
     */
    private ConceptGenResponse conceptMatches;
    /**
     * List of Artifact IDs that experience a contradiction with target artifact.
     */
    private List<String> conflictingIds;
    /**
     * Links of project artifacts to target artifact.
     */
    private List<GenerationLink> contextTraces;
}
