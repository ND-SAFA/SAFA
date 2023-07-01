package edu.nd.crc.safa.features.hgen;

import java.util.List;
import java.util.UUID;
import javax.annotation.Nullable;
import javax.validation.constraints.NotNull;

import edu.nd.crc.safa.features.tgen.api.requests.AbstractGenerationRequest;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Request to generate hierarchy for artifacts.
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Data
@NoArgsConstructor
public class HGenRequestDTO extends AbstractGenerationRequest {
    /**
     * List of artifact ids to generate hierarchy for.
     */
    @NotNull
    List<UUID> artifacts;
    /**
     * The target type of artifact to create.
     */
    @NotNull
    String targetType;
    /**
     * List of lists representing clusters.
     */
    @Nullable
    List<List<String>> clusters;
}
