package edu.nd.crc.safa.server.entities.app;

/**
 * Enumerates the type of nodes in a fault-tree analysis (FTA).
 */
public enum FTANodeType {
    OR {
        public String toString() {
            return "OR";
        }
    },
    AND {
        public String toString() {
            return "AND";
        }
    }
}
