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
     * The user initiating the change.
     */
    String user;
    /**
     * The change that should be resolved by client.
     */
    List<Change> changes = new ArrayList<>();
    /**
     * Whether the changes included in the message invalidate
     * the default document layout.
     */
    boolean updateLayout = false;

    @JsonIgnore
    public Change getChangeForEntity(Change.Entity entity) {
        List<Change> changeQuery = changes
            .stream()
            .filter(c -> c.getEntity().equals(entity))
            .collect(Collectors.toList());
        assert !changeQuery.isEmpty();
        assert changeQuery.size() <= 1;
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

    public void addChange(Change change) {
        this.changes.add(change);
    }
}
