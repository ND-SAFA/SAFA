package edu.nd.crc.safa.features.projects.entities.app;

/**
 * Responsible for enumerating all the possible entities that can
 * be updated via notifications.
 */
public enum ProjectEntityTypes {
    MEMBERS,
    TYPES;

    @Override
    public String toString() {
        return this.name();
    }
}
