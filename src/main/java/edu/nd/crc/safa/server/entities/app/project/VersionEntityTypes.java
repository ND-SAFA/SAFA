package edu.nd.crc.safa.server.entities.app.project;

/**
 * Responsible for enumerating all the possible versioned entities
 * that can be updated via notifications.
 */
public enum VersionEntityTypes {
    VERSION,
    ARTIFACTS,
    TRACES,
    WARNINGS;

    @Override
    public String toString() {
        return this.name();
    }
}
