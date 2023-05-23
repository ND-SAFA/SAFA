package edu.nd.crc.safa.features.tgen.entities;

import java.util.UUID;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Task identifier response.
 */
@Data
@NoArgsConstructor
public class TGenTask {
    /**
     * UUID for task subitted to TGEN.
     */
    @JsonProperty("task_id")
    UUID taskId;
}
