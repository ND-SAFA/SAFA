package edu.nd.crc.safa.features.health;

import edu.nd.crc.safa.features.generation.common.GenerationDataset;

import lombok.AllArgsConstructor;
import lombok.Data;

@AllArgsConstructor
@Data
public class HealthGenRequest {
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
