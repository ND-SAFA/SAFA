package edu.nd.crc.safa.features.prompt;

import edu.nd.crc.safa.features.tgen.entities.BaseGenerationModels;

import lombok.Data;

/**
 * Request to complete prompt with LLM model.
 */
@Data
public class TGenPromptRequest {
    /**
     * The model string to use. Either GPT or the path to a BERT model.
     */
    BaseGenerationModels model;
    /**
     * The prompt to complete.
     */
    String prompt;
}
