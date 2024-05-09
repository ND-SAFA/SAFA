package edu.nd.crc.safa.features.health.entities.gen;

import edu.nd.crc.safa.features.generation.common.GenerationDataset;

import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;
import lombok.AllArgsConstructor;
import lombok.Data;

@AllArgsConstructor
@Data
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public class GenHealthRequest {
    /**
     * List of artifacts in project.
     */
    private GenerationDataset dataset;
    /**
     * ID of artifact representing the target artifac.t
     */
    private String queryId;
    /**
     * Target artifact to generate health checks for.
     */
    private String conceptLayerId;
}
