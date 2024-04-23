package edu.nd.crc.safa.features.chat.entities.dtos;

import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;

@AllArgsConstructor
@Data
public class SendMessageResponseDTO {
    @NotNull
    private ChatMessageDTO userMessage;
    @NotNull
    private ChatMessageDTO responseMessage;
}
