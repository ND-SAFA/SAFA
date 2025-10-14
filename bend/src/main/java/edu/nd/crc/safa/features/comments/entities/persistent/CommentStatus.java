package edu.nd.crc.safa.features.comments.entities.persistent;

import com.fasterxml.jackson.annotation.JsonValue;

public enum CommentStatus {
    /**
     * Default state of comment.
     */
    ACTIVE,
    /**
     * Will allow comment to be hidden.
     */
    RESOLVED;

    @JsonValue
    public String toLower() {
        return this.name().toLowerCase();
    }

    /**
     * Toggles the status of the comment.
     *
     * @return New comment status.
     */
    public CommentStatus toggle() {
        return this.equals(ACTIVE) ? RESOLVED : ACTIVE;
    }
}
