package edu.nd.crc.safa.features.comments.entities.persistent;

public enum CommentType {
    /**
     * Comment left by another user.
     */
    CONVERSATION,
    /**
     * Flag left by another user.
     */
    FLAG,
    /**
     * AI generated contradiction with other artifacts.
     */
    CONTRADICTION,
    /**
     * Generated notification that a concept in artifact is not found in project vocabulary.
     */
    UNKNOWN_CONCEPT,
    /**
     * Generated notification that a concept in project vocabulary was matched.
     */
    MATCHED_CONCEPT,
    /**
     * Generated notification that a concept in artifact was matched with multiple.
     */
    MULTI_MATCHED_CONCEPT
}
