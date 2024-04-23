package edu.nd.crc.safa.features.chat.entities.dtos;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.chat.entities.persistent.ChatMessage;

import jakarta.annotation.Nullable;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;

@AllArgsConstructor
@Data
public class ChatMessageDTO {
    @NotNull
    private UUID id;
    /**
     * The user message in chat.
     */
    private boolean isUser;
    /**
     * The AI message in chat.
     */
    @Nullable
    private String message;
    /**
     * Artifact ids associated with message.
     */
    @NotNull
    private List<UUID> artifactIds;

    /**
     * Creates DTO from response message.
     *
     * @param chatMessage The response message in chat.
     * @return DTO with copied fields.
     */
    public static ChatMessageDTO asResponseMessage(ChatMessage chatMessage, List<UUID> artifactIds) {
        return new ChatMessageDTO(
            chatMessage.getId(),
            false,
            chatMessage.getContent(),
            artifactIds);
    }

    /**
     * Creates DTO from user message.
     *
     * @param chatMessage The user message.
     * @return DTO with copied fields.
     */
    public static ChatMessageDTO asUserMessage(ChatMessage chatMessage) {
        return new ChatMessageDTO(
            chatMessage.getId(),
            true,
            chatMessage.getContent(),
            new ArrayList<>());
    }
}
