package edu.nd.crc.safa.features.generation.prompt;

import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.features.generation.common.ITGenResponse;

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

    @Override
    public List<String> getLogs() {
        return new ArrayList<>();
    }
}
