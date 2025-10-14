package edu.nd.crc.safa.features.health.entities;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import jakarta.validation.constraints.NotNull;
import lombok.Data;

@Data
public class HealthRequest {
    /**
     * Version of the artifacts to use.
     */
    @NotNull
    private UUID versionId;
    /**
     * List of health tasks to perform.
     */
    private List<HealthTask> tasks = new ArrayList<>();
    /**
     * Optional, if specified will make query artifacts those matching given types.
     */
    private List<String> artifactTypes = new ArrayList<>();
    /**
     * Optional, if given makes query artifacts those referenced.
     */
    private List<UUID> artifactIds = new ArrayList<>();
}
