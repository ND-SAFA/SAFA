package edu.nd.crc.safa.features.health.entities;

public enum HealthTask {
    /**
     * Finds contradictions existing within query artifacts.
     */
    CONTRADICTION,
    /**
     * Extracts missing concepts from query artifacts.
     */
    CONCEPT_EXTRACTION,
    /**
     * Matches concepts and artifacts that reference them.
     */
    CONCEPT_MATCHING
}
