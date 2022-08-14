package edu.nd.crc.safa.features.documents.entities.db;

import lombok.AllArgsConstructor;

/**
 * Enumeration of the type of documents a project may have.
 */
@AllArgsConstructor
public enum DocumentType {
    /**
     * Document containing only pure system artifacts.
     */
    ARTIFACT_TREE,
    /**
     * Document containing AND & OR nodes
     */
    FTA,
    /**
     * Document containing context, goals, strategies, and evidence.
     */
    SAFETY_CASE,
    /**
     * Document being represented in a table.
     */
    FMEA;

    @Override
    public String toString() {
        return this.name();
    }
}
