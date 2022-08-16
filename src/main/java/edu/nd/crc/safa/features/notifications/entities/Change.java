package edu.nd.crc.safa.features.notifications.entities;

import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

import lombok.AllArgsConstructor;
import lombok.Data;

/**
 * A modification made to an entity and the necessary action
 * to synchronize front-end.
 */
@AllArgsConstructor
@Data
public class Change {
    /**
     * The entity that was changed.
     */
    Entity entity;
    /**
     * The type of change applied to entity.
     */
    Action action;
    /**
     * ID of entity changed.
     */
    List<UUID> entityIds;

    public List<String> getStringEntityIds() {
        return this.entityIds.stream().map(UUID::toString).collect(Collectors.toList());
    }

    /**
     * Represents the action necessary to update entity in notification
     */
    public enum Action {
        DELETE,
        UPDATE;

        @Override
        public String toString() {
            return this.name();
        }
    }

    /**
     * The entity changed in change.
     */
    public enum Entity {
        PROJECT,
        MEMBERS,
        VERSION,
        TYPES,
        DOCUMENT,
        ARTIFACTS,
        TRACES,
        WARNINGS;

        @Override
        public String toString() {
            return this.name();
        }
    }
}
