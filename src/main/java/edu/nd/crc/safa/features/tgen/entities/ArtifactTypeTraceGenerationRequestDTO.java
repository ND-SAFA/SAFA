package edu.nd.crc.safa.features.tgen.entities;

import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Represents a request to generate links between two artifact types;
 */
@AllArgsConstructor
@NoArgsConstructor
@Data
public class ArtifactTypeTraceGenerationRequestDTO {
    /**
     * The algorithm for generating similarity scores in trace links.
     */
    @NotNull
    @NotEmpty
    TraceGenerationMethod method = TraceGenerationMethod.getDefault();
    /**
     * The name of the artifact type for source artifacts.
     */
    @NotNull
    @NotEmpty
    String source;
    /**
     * The name of the artifact type for target artifacts.
     */
    @NotNull
    @NotEmpty
    String target;
}
