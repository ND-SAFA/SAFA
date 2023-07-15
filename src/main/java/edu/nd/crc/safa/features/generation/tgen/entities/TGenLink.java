package edu.nd.crc.safa.features.generation.tgen.entities;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Data;

/**
 * A predicted trace link.
 */
@JsonIgnoreProperties(ignoreUnknown = true)
@Data
public class TGenLink {
    String source;
    String target;
    double score;
    double label = -1;
    String classification;
}
