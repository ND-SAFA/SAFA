package edu.nd.crc.safa.features.chat.entities.dtos;

import java.util.UUID;

import edu.nd.crc.safa.features.chat.entities.persistent.Chat;

import jakarta.annotation.Nullable;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

@Data
public class ChatDTO {
    @Nullable
    private UUID id;
    /**
     * Display name of chat.
     */
    @Nullable
    private String title;
    /**
     * ID of version being accessed during chat.
     */
    @NotNull
    private UUID versionId;

    /**
     * Creates DTO (application entity) from Chat (persistent entity).
     *
     * @param chat The persisted chat to copy fields to DTO.
     * @return ChatDTO with fields copied from Chat.
     */
    public static ChatDTO fromChat(Chat chat) {
        ChatDTO chatDTO = new ChatDTO();
        chatDTO.setId(chat.getId());
        chatDTO.setTitle(chat.getTitle());
        chatDTO.setVersionId(chat.getProjectVersion().getVersionId());
        return chatDTO;
    }
}
