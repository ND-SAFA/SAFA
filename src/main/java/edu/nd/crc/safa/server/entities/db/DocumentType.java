package edu.nd.crc.safa.server.entities.db;

/**
 * Enumeration of the type of documents a project may have.
 */
public enum DocumentType {
    /**
     * Nodes represented to exist throughout all documents in the project.
     */
    ARTIFACT_TREE {
        public String toString() {
            return "ARTIFACT_TREE";
        }
    },
    /**
     * Nodes used only in fault tree analysis documents.
     */
    FTA {
        public String toString() {
            return "FTA";
        }
    },
    /**
     * Nodes used only in safety case documents.
     */
    SAFETY_CASE {
        public String toString() {
            return "SAFETY_CASE";
        }
    }
}
