package edu.nd.crc.safa.features.documents.entities.app;

/**
 * Represents the types of data that a column can have.
 */
public enum DocumentColumnDataType {

    /**
     * Represents a column containing any user defined text body.
     */
    FREE_TEXT,
    /**
     * References the id of a row of another table.
     */
    RELATION,
    /**
     * References an enumerate value
     */
    SELECT;

    @Override
    public String toString() {
        return this.name();
    }
}
