package edu.nd.crc.safa.features.chat.entities.gen;

import java.util.ArrayList;
import java.util.List;

import edu.nd.crc.safa.features.chat.entities.persistent.ChatMessage;

import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;
import lombok.Data;
import lombok.NoArgsConstructor;

@NoArgsConstructor
@Data
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public class GenChatMessage {
    /**
     * Content of chat message
     */
    private String content;
    /**
     * Either "assistant"
     */
    private GenChatRole role;
    /**
     * Artifact Ids used in chat.
     */
    private List<String> artifactIds = new ArrayList<>();

    /**
     * Constructs Gen message from ChatMessage (persistent).
     *
     * @param chatMessage The persisted chat message.
     * @param artifactIds The artifact ids used in the construction of this message.
     */
    public GenChatMessage(ChatMessage chatMessage, List<String> artifactIds) {
        this.role = GenChatRole.fromIsUser(chatMessage.isUser());
        this.content = chatMessage.getContent();
        this.artifactIds = artifactIds;
    }

    /**
     * Creates GenChatMessage for user with given content.
     *
     * @param content The content of the message.
     * @return GenChatMessage instance.
     */
    public static GenChatMessage fromUserMessage(String content) {
        GenChatMessage msg = new GenChatMessage();
        msg.role = GenChatRole.USER;
        msg.content = content;
        return msg;
    }
}
