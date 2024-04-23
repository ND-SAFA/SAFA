package edu.nd.crc.safa.features.chat.entities.dtos;

import jakarta.validation.constraints.NotNull;
import lombok.Data;

@Data
public class SendChatMessageRequest {

    /**
     * The user message in chat.
     */
    @NotNull
    private String message;
}
