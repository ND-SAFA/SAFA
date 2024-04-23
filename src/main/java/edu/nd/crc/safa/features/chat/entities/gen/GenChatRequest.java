package edu.nd.crc.safa.features.chat.entities.gen;

import java.util.List;

import edu.nd.crc.safa.features.chat.entities.persistent.ChatMessage;
import edu.nd.crc.safa.features.generation.common.GenerationArtifact;

import lombok.Data;

@Data
public class GenChatRequest {
    /**
     * User message that AI is responding to.
     */
    private String message;
    /**
     * Artifacts used in context of response.
     */
    private List<GenerationArtifact> artifacts;
    /**
     * Previous messages in conversation.
     */
    private List<ChatMessage> messages;
}
