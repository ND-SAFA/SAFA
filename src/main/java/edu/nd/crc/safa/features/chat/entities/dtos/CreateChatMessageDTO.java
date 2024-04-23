package edu.nd.crc.safa.features.chat.entities.dtos;

import jakarta.validation.constraints.NotNull;
import lombok.Data;

@Data
public class CreateChatMessageDTO {

    @NotNull
    private String message;
}
