package edu.nd.crc.safa.features.prompt;

import edu.nd.crc.safa.features.tgen.api.requests.AbstractGenerationRequest;

import lombok.Data;

/**
 * Request to complete prompt with LLM model.
 */
@Data
public class TGenPromptRequest extends AbstractGenerationRequest {
    /**
     * The prompt to complete.
     */
    String prompt;
}
