package edu.nd.crc.safa.features.generation.common;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Represents a set of traced layers in a dataset.
 */
@NoArgsConstructor
@AllArgsConstructor
@Data
public class TraceLayer {
    /**
     * The child type in tracing.
     */
    private String child;
    /**
     * The parent type in tracing.
     */
    private String parent;
}
