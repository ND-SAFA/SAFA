package edu.nd.crc.safa.features.health.entities;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@AllArgsConstructor
@NoArgsConstructor
@Data
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
@JsonIgnoreProperties(ignoreUnknown = true)
public class ConceptMatchDTO {
    /**
     * The artifact ID containing concept ID
     */
    private String artifactId;
    /**
     * ID of concept artifact matched.
     */
    private String conceptId;
    /**
     * Index of start of match string.
     */
    private int startLoc;
    /**
     * Index of end of match string.
     */
    private int endLoc;
}
