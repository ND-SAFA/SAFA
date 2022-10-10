package edu.nd.crc.safa.features.tgen.entities.api;

import java.util.HashMap;
import java.util.List;
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
    List<Map<String, String>> sourceLayers;
    /**
     * Map of target artifact ids to content body.
     */
    List<Map<String, String>> targetLayers;
    /**
     * Map of custom key-value pairs to set on trainer
     */
    Map<String, String> settings = new HashMap<>();
}
