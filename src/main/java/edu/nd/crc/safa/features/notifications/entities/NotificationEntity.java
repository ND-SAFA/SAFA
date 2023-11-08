package edu.nd.crc.safa.features.notifications.entities;

/**
 * The entity changed in change.
 */
public enum NotificationEntity {
    PROJECT,
    MEMBERS,
    ACTIVE_MEMBERS,
    VERSION,
    TYPES,
    DOCUMENT,
    ARTIFACTS,
    LAYOUT,
    ATTRIBUTES,
    TRACES,
    WARNINGS,
    JOBS,
    TRACE_MATRICES;

    @Override
    public String toString() {
        return this.name();
    }
}
