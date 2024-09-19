package edu.nd.crc.safa.features.health.entities.gen;

import java.util.List;

import edu.nd.crc.safa.features.generation.common.GenerationDataset;
import edu.nd.crc.safa.features.health.entities.HealthTask;

import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;
import lombok.AllArgsConstructor;
import lombok.Data;

@AllArgsConstructor
@Data
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public class GenHealthRequest {
    /**
     * The health tasks to perform on query artifacts.
     */
    private List<HealthTask> tasks;
    /**
     * List of artifacts in project.
     */
    private GenerationDataset dataset;
    /**
     * ID of artifact representing the target artifac.t
     */
    private List<String> queryIds;
    /**
     * Target artifact to generate health checks for.
     */
    private String conceptLayerId;
}
