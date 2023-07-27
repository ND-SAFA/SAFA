package edu.nd.crc.safa.features.generation.common;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Data;

/**
 * A predicted trace link.
 */
@JsonIgnoreProperties(ignoreUnknown = true)
@Data
public class GenerationLink {
    /**
     * The child name;
     */
    String source;
    /**
     * The parent name.
     */
    String target;
    /**
     * The similarity score.
     */
    double score;
    /**
     * The true label between them.
     */
    double label = -1;
    /**
     * The trace explanation.
     */
    String explanation;
}
