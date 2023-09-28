package edu.nd.crc.safa.features.generation.hgen;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import com.fasterxml.jackson.annotation.JsonInclude;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotNull;
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
    private List<UUID> artifacts = new ArrayList<>();
    /**
     * The target type of artifact to create.
     */
    @NotNull
    @Valid
    private List<@Valid String> targetTypes = new ArrayList<>();
    /**
     * Optional. Project summary.
     */
    private String summary;
}
