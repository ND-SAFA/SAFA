package edu.nd.crc.safa.features.notifications.entities;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.IUser;

import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Notification message for automatic updates of entities.
 * Contains list of entities that need updated.
 */
@NoArgsConstructor
@Data
public class EntityChangeMessage {
    /**
     * The user initiating the change.
     */
    private UUID userId;
    /**
     * Project ID | Version ID | Job ID
     */
    private String topic;
    /**
     * The change that should be resolved by client.
     */
    private List<Change> changes = new ArrayList<>();
    /**
     * Whether the changes included in the message invalidate
     * the default document layout.
     */
    private boolean updateLayout = false;

    public EntityChangeMessage(IUser user, Change change) {
        this.userId = user.getUserId();
        this.changes.add(change);
    }

    @JsonIgnore
    public Change getChangeForEntity(NotificationEntity entity) {
        List<Change> changeQuery = changes
            .stream()
            .filter(c -> c.getEntity().equals(entity))
            .collect(Collectors.toList());
        if (changeQuery.size() > 1) {
            throw new SafaError("Unexpected single change for %s but found %s", entity, changeQuery.size());
        }
        if (changeQuery.isEmpty()) {
            throw new SafaError("Found no changes (%s) with entity %s.", this.changes.size(), entity);
        }
        return changeQuery.get(0);
    }

    public void addChange(Change change) {
        this.changes.add(change);
    }
}
