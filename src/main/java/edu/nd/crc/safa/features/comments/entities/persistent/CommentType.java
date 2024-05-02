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
    UNDEFINED_CONCEPT,
    /**
     * Concept was found directly cited in artifact.
     */
    CITED_CONCEPT,
    /**
     * Concept was predicted to be used in artifact.
     */
    PREDICTED_CONCEPT,
    /**
     * Generated notification that a concept in artifact was matched with multiple.
     */
    MULTI_MATCHED_CONCEPT
}
