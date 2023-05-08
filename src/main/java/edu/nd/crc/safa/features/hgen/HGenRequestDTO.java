package edu.nd.crc.safa.features.hgen;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.tgen.entities.api.AbstractGenerationRequest;

import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Request to generate hierarchy for artifacts.
 */
@Data
@NoArgsConstructor
public class HGenRequestDTO extends AbstractGenerationRequest {
    /**
     * List of artifact ids to generate hierarchy for.
     */
    List<UUID> artifacts;
}
