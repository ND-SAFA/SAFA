package edu.nd.crc.safa.features.generation.common;

import lombok.AllArgsConstructor;
import lombok.Data;

/**
 * Represents a set of traced layers in a dataset.
 */
@AllArgsConstructor
@Data
public class TraceLayer {
    /**
     * The child type in tracing.
     */
    String child;
    /**
     * The parent type in tracing.
     */
    String parent;
}
