package edu.nd.crc.safa.features.chat.entities.dtos;

import lombok.Data;

@Data
public class EditChatRequestDTO {
    /**
     * New title for chat.
     */
    private String title;
}
