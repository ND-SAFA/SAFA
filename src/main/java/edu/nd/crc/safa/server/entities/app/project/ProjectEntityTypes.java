package edu.nd.crc.safa.server.entities.app.project;

/**
 * Responsible for enumerating all the possible entities that can
 * be updated via notifications.
 */
public enum ProjectEntityTypes {
    DOCUMENTS,
    MEMBERS,
    TYPES;

    @Override
    public String toString() {
        return this.name();
    }
}
