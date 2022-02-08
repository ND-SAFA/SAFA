package edu.nd.crc.safa.server.entities.db;

/**
 * Enumeration of the type of documents a project may have.
 */
public enum DocumentType {
    ARTIFACT_TREE {
        public String toString() {
            return "ARTIFACT_TREE";
        }
    },
    FTA {
        public String toString() {
            return "FTA";
        }
    },
}
