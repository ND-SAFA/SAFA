package edu.nd.crc.safa.features.comments.entities.persistent;

import com.fasterxml.jackson.annotation.JsonValue;
import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Getter;

@AllArgsConstructor(access = AccessLevel.PRIVATE)
@Getter
public enum CommentType {
    /**
     * Comment left by another user.
     */
    CONVERSATION(false),
    /**
     * Flag left by another user.
     */
    FLAG(false),
    /**
     * AI generated contradiction with other artifacts.
     */
    CONTRADICTION(true),
    /**
     * Generated notification that a concept in artifact is not found in project vocabulary.
     */
    UNDEFINED_CONCEPT(true),
    /**
     * Concept was found directly cited in artifact.
     */
    CITED_CONCEPT(true),
    /**
     * Concept was predicted to be used in artifact.
     */
    PREDICTED_CONCEPT(true),
    /**
     * Generated notification that a concept in artifact was matched with multiple.
     */
    MULTI_MATCHED_CONCEPT(true);
    /**
     * Whether comment type is a health check.
     */
    private final boolean isHealthCheck;

    @JsonValue
    public String toLower() {
        return this.name().toLowerCase();
    }
}
