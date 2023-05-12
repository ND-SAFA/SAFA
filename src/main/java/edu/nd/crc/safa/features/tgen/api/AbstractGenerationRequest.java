package edu.nd.crc.safa.features.tgen.api;

import edu.nd.crc.safa.features.tgen.entities.BaseGenerationModels;

import lombok.Data;

@Data
public class AbstractGenerationRequest {
    /**
     * The model string to use. Either GPT or the path to a BERT model.
     */
    BaseGenerationModels model;

    /**
     * @return Returns the base generation model associated with request.
     */
    public BaseGenerationModels getModel() {
        return this.model == null ? BaseGenerationModels.getDefault() : model;
    }
}
