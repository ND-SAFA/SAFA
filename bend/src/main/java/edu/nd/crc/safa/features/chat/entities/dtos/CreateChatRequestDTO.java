package edu.nd.crc.safa.features.chat.entities.dtos;

import java.util.UUID;

import lombok.Data;

@Data
public class CreateChatRequestDTO {
    public static final String DEFAULT_TITLE = "Untitled Chat";
    /**
     * Version ID to use artifacts in chat.
     */
    private UUID versionId;
    /**
     * The title of the chat.
     */
    private String title;

    /**
     * Sets title to default title if empty or blank.
     *
     * @param title Title of the chat.
     */
    public void setTitle(String title) {
        this.title = title == null || title.isBlank() ? DEFAULT_TITLE : title;
    }
}
