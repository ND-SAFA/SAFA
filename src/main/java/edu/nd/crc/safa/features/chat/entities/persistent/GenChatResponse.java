package edu.nd.crc.safa.features.chat.entities.persistent;

import java.util.List;

import lombok.Data;

/**
 * Gen response to chat request.
 */
@Data
public class GenChatResponse {
    /**
     * The message the AI responded with.
     */
    private String message;
    /**
     * The artifact IDs used to cite
     */
    private List<String> artifactIds;
}
