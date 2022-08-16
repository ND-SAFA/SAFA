package edu.nd.crc.safa.features.versions.entities.app;

/**
 * Responsible for enumerating all the possible versioned entities
 * that can be updated via notifications.
 */
public enum VersionEntityTypes {
    VERSION,
    ARTIFACTS,
    TRACES,
    WARNINGS,
    DOCUMENTS;

    @Override
    public String toString() {
        return this.name();
    }
}
