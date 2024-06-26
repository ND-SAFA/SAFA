package edu.nd.crc.safa.features.health.entities.gen;

import java.util.List;

import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;
import lombok.AllArgsConstructor;
import lombok.Data;

@AllArgsConstructor
@Data
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public class GenUndefinedEntity {
    /**
     * Ids of artifacts referencing undefined entity.
     */
    private List<String> artifactIds;
    /**
     * Name of concept, used as ID.
     */
    private String conceptId;
    /**
     * Predicted definition of undefined concept.
     */
    private String conceptDefinition;
}
