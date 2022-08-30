package edu.nd.crc.safa.features.tgen.entities;

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
    TraceGenerationMethod traceGenerationMethod = TraceGenerationMethod.VSM;
    /**
     * The name of the artifact type for source artifacts.
     */
    String sourceTypeName;
    /**
     * The name of the artifact type for target artifacts.
     */
    String targetTypeName;
}
