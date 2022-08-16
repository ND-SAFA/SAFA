package edu.nd.crc.safa.features.notifications.entities;

import java.util.ArrayList;
import java.util.List;

import lombok.Data;

/**
 * Notification message for automatic updates of entities.
 * Contains list of entities that need updated.
 */
@Data
public class EntityChangeMessage {

    /**
     * The change that should be resolved by client.
     */
    List<Change> changes = new ArrayList<>();
    /**
     * The user initiating the change.
     */
    String user;
    /**
     * Whether to update the default layout of the project.
     */
    boolean updateLayout = false;

    public boolean shouldUpdateLayout() {
        List<Change.Entity> entitiesTriggeringLayout = List.of(
            Change.Entity.ARTIFACTS,
            Change.Entity.TRACES,
            Change.Entity.VERSION);
        return this.changes
            .stream()
            .map(Change::getEntity)
            .anyMatch(entitiesTriggeringLayout::contains);
    }
}
