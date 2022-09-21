package edu.nd.crc.safa.features.tgen.entities;

import java.util.Map;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * The payload to the prediction endpoint of TGEN.
 */
@NoArgsConstructor
@AllArgsConstructor
@Data
public class TGenPredictionRequestDTO {
    /**
     * The folder container the prediction on the TGEN bucket.
     */
    final String outputDir = "prediction/output";
    /**
     * The base model architecture.
     */
    String baseModel;
    /**
     * Path to model weights.
     */
    String modelPath;
    /**
     * Whether to load model state from cloud storage.
     */
    boolean loadFromStorage;
    /**
     * Map of source artifact ids to content body.
     */
    Map<String, String> sources;
    /**
     * Map of target artifact ids to content body.
     */
    Map<String, String> targets;
}
