package edu.nd.crc.safa.features.prompt;

import java.util.List;

import edu.nd.crc.safa.features.tgen.api.responses.ITGenResponse;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * The response for a prompt completion request.
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
public class TGenPromptResponse implements ITGenResponse {
    /**
     * The completion to prompt.
     */
    String completion;
    List<String> logs;
}
