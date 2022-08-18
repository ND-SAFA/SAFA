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
public class TraceGenerationRequest {
    String source;
    String target;
}
