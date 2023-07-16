package edu.nd.crc.safa.features.generation.common;

import lombok.AllArgsConstructor;
import lombok.Data;

@AllArgsConstructor
@Data
public class TGenLayer {
    /**
     * The child type in tracing.
     */
    String child;
    /**
     * The parent type in tracing.
     */
    String parent;
}
