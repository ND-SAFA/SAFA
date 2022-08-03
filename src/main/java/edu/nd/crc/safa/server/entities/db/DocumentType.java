package edu.nd.crc.safa.server.entities.db;

import lombok.AllArgsConstructor;

/**
 * Enumeration of the type of documents a project may have.
 */
@AllArgsConstructor
public enum DocumentType {
    /**
     * Document containing only pure system artifacts.
     */
    ARTIFACT_TREE("ARTIFACT_TREE"),
    /**
     * Document containing AND & OR nodes
     */
    FTA("FTA"),
    /**
     * Document containing context, goals, strategies, and evidence.
     */
    SAFETY_CASE("SAFETY_CASE"),
    /**
     * Document being represented in a table.
     */
    FMEA("FMEA");

    private String value;

    @Override
    public String toString() {
        return this.value;
    }
}
