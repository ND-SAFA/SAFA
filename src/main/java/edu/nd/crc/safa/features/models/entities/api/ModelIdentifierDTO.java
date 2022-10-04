package edu.nd.crc.safa.features.models.entities.api;

import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Represents a request to create a tranformers model.
 */
@NoArgsConstructor
@Data
public class ModelIdentifierDTO {

    /**
     * The base model class to create model from.
     */
    String baseModel;
    /**
     * The status of the request.
     */
    int status;
    /**
     * The state of the model base class containing starting weights.
     */
    String modelPath;
    /**
     * The path to the output file within storage.
     */
    String outputDir;

    public ModelIdentifierDTO(String baseModel, String modelPath, String outputDir) {
        this.baseModel = baseModel;
        this.modelPath = modelPath;
        this.outputDir = outputDir;
    }
}
