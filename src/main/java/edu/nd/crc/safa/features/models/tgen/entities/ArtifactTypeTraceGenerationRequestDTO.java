package edu.nd.crc.safa.features.models.tgen.entities;

import javax.validation.constraints.NotNull;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

/**
 * Represents a request to generate links between two artifact types;
 */
@EqualsAndHashCode(callSuper = true)
@AllArgsConstructor
@NoArgsConstructor
@Data
public class ArtifactTypeTraceGenerationRequestDTO extends ArtifactLevelRequest {
    /**
     * The algorithm for generating similarity scores in trace links.
     */
    @NotNull
    BaseGenerationModels method = BaseGenerationModels.getDefault();
}
