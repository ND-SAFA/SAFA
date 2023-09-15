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
    private String source;
    /**
     * The parent name.
     */
    private String target;
    /**
     * The similarity score.
     */
    private double score;
    /**
     * The true label between them.
     */
    private double label = -1;
    /**
     * The trace explanation.
     */
    private String explanation;
}
