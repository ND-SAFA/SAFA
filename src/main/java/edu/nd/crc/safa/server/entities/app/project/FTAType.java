package edu.nd.crc.safa.server.entities.app.project;

/**
 * Enumerates the type of nodes in a fault-tree analysis (FTA).
 */
public enum FTAType {
    OR,
    AND;

    @Override
    public String toString() {
        return this.name();
    }
}
