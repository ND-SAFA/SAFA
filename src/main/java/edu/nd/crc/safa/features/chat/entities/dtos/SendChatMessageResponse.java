package edu.nd.crc.safa.features.chat.entities.dtos;

import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;

/**
 * Messages created during message send.
 */
@AllArgsConstructor
@Data
public class SendChatMessageResponse {
    /**
     * The user message created.
     */
    @NotNull
    private ChatMessageDTO userMessage;
    /**
     * Response message.
     */
    @NotNull
    private ChatMessageDTO responseMessage;
}
