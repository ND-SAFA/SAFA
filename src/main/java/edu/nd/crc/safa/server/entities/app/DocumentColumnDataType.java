package edu.nd.crc.safa.server.entities.app;

/**
 * Represents the types of data that a column can have.
 */
public enum DocumentColumnDataType {

    /**
     * Represents a column containing any user defined text body.
     */
    FREE_TEXT {
        public String toString() {
            return "FREE_TEXT";
        }
    },
    /**
     * References the id of a row of another table.
     */
    RELATION {
        public String toString() {
            return "RELATION";
        }
    },
    /**
     * References an enumerate value
     */
    SELECT {
        public String toString() {
            return "SELECT";
        }
    }
}
