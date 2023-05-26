package edu.nd.crc.safa.features.prompt;

import edu.nd.crc.safa.features.tgen.api.AbstractTGenResponse;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * The response for a prompt completion request.
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
public class TGenPromptResponse extends AbstractTGenResponse {
    /**
     * The completion to prompt.
     */
    String completion;
}
