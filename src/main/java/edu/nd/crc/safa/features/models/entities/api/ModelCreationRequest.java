package edu.nd.crc.safa.features.models.entities.api;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Represents a request to create a tranformers model.
 */
@NoArgsConstructor
@AllArgsConstructor
@Data
public class ModelCreationRequest {

    /**
     * The base model class to create model from.
     */
    String baseModelClass;
    /**
     * The state of the model base class containing starting weights.
     */
    String statePath;
    /**
     * The path to the output file within storage.
     */
    String outputPath;
}
