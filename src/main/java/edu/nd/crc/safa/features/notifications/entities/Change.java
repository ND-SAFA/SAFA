package edu.nd.crc.safa.features.notifications.entities;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * A modification made to an entity and the necessary action
 * to synchronize front-end.
 */
@NoArgsConstructor
@AllArgsConstructor
@Data
public class Change {
    /**
     * The entity that was changed.
     */
    private Entity entity;
    /**
     * The type of change applied to entity.
     */
    private Action action;
    /**
     * ID of entity changed.
     */
    private List<UUID> entityIds = new ArrayList<>();

    private List<Object> entities = new ArrayList<>();

    public <T extends Object> void setEntities(List<T> entities) {
        this.entities = (List<Object>) entities;
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
        ACTIVE_MEMBERS,
        VERSION,
        TYPES,
        DOCUMENT,
        ARTIFACTS,
        TRACES,
        WARNINGS,
        JOBS,
        TRACE_MATRICES;

        @Override
        public String toString() {
            return this.name();
        }
    }
}
