package edu.nd.crc.safa.features.generation.prompt;

import lombok.Data;

/**
 * Request to complete prompt with LLM model.
 */
@Data
public class TGenPromptRequest {
    /**
     * The prompt to complete.
     */
    private String prompt;
}
