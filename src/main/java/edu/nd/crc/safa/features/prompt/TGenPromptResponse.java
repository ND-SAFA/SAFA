package edu.nd.crc.safa.features.prompt;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * The response for a prompt completion request.
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
public class TGenPromptResponse {
    /**
     * The completion to prompt.
     */
    String completion;
}
