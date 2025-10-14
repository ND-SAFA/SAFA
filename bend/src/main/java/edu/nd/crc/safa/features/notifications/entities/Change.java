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
    private NotificationEntity entity;
    /**
     * The type of change applied to entity.
     */
    private NotificationAction action;
    /**
     * ID of entity changed.
     */
    private List<UUID> entityIds = new ArrayList<>();

    private List<Object> entities = new ArrayList<>();

    public <T extends Object> void setEntities(List<T> entities) {
        assert entities != null;
        this.entities = (List<Object>) entities;
    }

    public void setEntityIds(List<UUID> entityIds) {
        assert entityIds != null;
        this.entityIds = entityIds;
    }
}
