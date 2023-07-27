package edu.nd.crc.safa.features.generation.hgen;

import java.util.List;
import java.util.UUID;
import javax.validation.Valid;
import javax.validation.constraints.NotNull;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Request to generate hierarchy for artifacts.
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Data
@NoArgsConstructor
public class HGenRequest {
    /**
     * List of artifact ids to generate hierarchy for.
     */
    @NotNull
    List<UUID> artifacts;
    /**
     * The target type of artifact to create.
     */
    @NotNull
    @Valid List<@Valid String> targetTypes;
    /**
     * Optional. Project summary.
     */
    String summary;
}
