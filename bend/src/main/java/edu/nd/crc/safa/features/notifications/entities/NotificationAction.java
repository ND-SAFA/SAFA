package edu.nd.crc.safa.features.notifications.entities;

/**
 * Represents the action necessary to update entity in notification
 */
public enum NotificationAction {
    DELETE,
    UPDATE;

    @Override
    public String toString() {
        return this.name();
    }
}
