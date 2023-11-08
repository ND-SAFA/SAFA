package edu.nd.crc.safa.features.projects.entities.db;

/**
 * The type of activities occurring while parsing a project.
 */
public enum ProjectEntityType {
    TIM,
    ARTIFACTS,
    TRACES;

    @Override
    public String toString() {
        return this.name();
    }
}
