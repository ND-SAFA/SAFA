package edu.nd.crc.safa.features.artifacts.entities;

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
