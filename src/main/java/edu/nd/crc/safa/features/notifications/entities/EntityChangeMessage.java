package edu.nd.crc.safa.features.notifications.entities;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

import com.fasterxml.jackson.annotation.JsonIgnore;
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

    @JsonIgnore
    public Change getChangeForEntity(Change.Entity entity) {
        List<Change> changeQuery = changes
            .stream()
            .filter(c -> c.getEntity().equals(entity))
            .collect(Collectors.toList());
        assert changeQuery.size() == 1;
        return changeQuery.get(0);
    }

    /**
     * Returns list of entities changed in message.
     *
     * @return List of {@link Change.Entity}, one per change.
     */
    @JsonIgnore
    public List<Change.Entity> getChangedEntities() {
        return this.changes.stream().map(Change::getEntity).collect(Collectors.toList());
    }
}
