package edu.nd.crc.safa.server.entities.db;

/**
 * Enumeration of the type of documents a project may have.
 */
public enum DocumentType {
    /**
     * Document containing only pure system artifacts.
     */
    ARTIFACT_TREE {
        public String toString() {
            return "ARTIFACT_TREE";
        }
    },
    /**
     * Document containing system artifacts and the nodes for
     * conducting a fault tree analysis.
     */
    FTA {
        public String toString() {
            return "FTA";
        }
    },
    /**
     * Document containing system artifacts and nodes required
     * for constructing a safety case
     */
    SAFETY_CASE {
        public String toString() {
            return "SAFETY_CASE";
        }
    },

    /**
     * Document containing system artifacts containing custom fields
     * in a table
     */
    FMEA {
        public String toString() {
            return "FMEA";
        }
    },
}
