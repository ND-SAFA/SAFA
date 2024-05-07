package edu.nd.crc.safa.features.chat.entities.dtos;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.chat.entities.persistent.Chat;
import edu.nd.crc.safa.features.chat.entities.persistent.ChatPermission;

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
    private String title = "";
    /**
     * ID of version being accessed during chat.
     */
    @NotNull
    private UUID versionId;
    /**
     * Permission user has on chat.
     */
    private ChatPermission permission;
    /**
     * List of messages in chat.
     */
    private List<ChatMessageDTO> messages = new ArrayList<>();
    /**
     * Timestamp of last update to chat.
     */
    private LocalDateTime updatedAt;

    /**
     * Creates DTO (application entity) from Chat (persistent entity).
     *
     * @param chat       The persisted chat to copy fields to DTO.
     * @param permission The permission to attach to chat.
     * @return ChatDTO with fields copied from Chat.
     */
    public static ChatDTO fromChat(Chat chat, ChatPermission permission) {
        ChatDTO DTO = new ChatDTO();
        DTO.setId(chat.getId());
        DTO.setTitle(chat.getTitle());
        DTO.setVersionId(chat.getProjectVersion().getVersionId());
        DTO.setPermission(permission);
        DTO.setUpdatedAt(chat.getUpdatedAt());
        return DTO;
    }

    /**
     * Sets title to empty string if null given.
     *
     * @param title Title of the chat.
     */
    public void setString(String title) {
        this.title = title == null ? "" : title;
    }
}
