package edu.nd.crc.safa.server.entities.app.project;

import lombok.AllArgsConstructor;

/**
 * Enumerates the types of nodes used in a safety case
 */
@AllArgsConstructor
public enum SafetyCaseType {
    SOLUTION,
    CONTEXT,
    GOAL,
    STRATEGY;

    @Override
    public String toString() {
        return this.name();
    }
}
