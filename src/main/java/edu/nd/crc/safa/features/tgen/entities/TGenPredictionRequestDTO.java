package edu.nd.crc.safa.features.tgen.entities;

import java.util.Map;

import lombok.AllArgsConstructor;
import lombok.Data;

/**
 * The payload to the prediction endpoint of TGEN.
 */
@AllArgsConstructor
@Data
public class TGenPredictionRequestDTO {
    /**
     * The base model architecture.
     */
    String baseModel;
    /**
     * Path to model weights.
     */
    String modelPath;
    /**
     * Map of source artifact ids to content body.
     */
    Map<String, String> sources;
    /**
     * Map of target artifact ids to content body.
     */
    Map<String, String> targets;
}
