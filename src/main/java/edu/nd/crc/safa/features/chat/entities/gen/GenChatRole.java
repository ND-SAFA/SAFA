package edu.nd.crc.safa.features.chat.entities.gen;

import com.fasterxml.jackson.annotation.JsonValue;

public enum GenChatRole {
    ASSISTANT,
    USER;

    /**
     * Utility constructor for constructing from chat message persistent object.
     *
     * @param isUser isUser flag on ChatMessage.
     * @return Associated Gen role.
     */
    public static GenChatRole fromIsUser(boolean isUser) {
        return isUser ? USER : ASSISTANT;
    }

    /**
     * @return Converts object to lower case JSON format.
     */
    @JsonValue
    public String toLower() {
        return this.name().toLowerCase();
    }
}
