package edu.nd.crc.safa.features.notifications.builders;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;

import lombok.AccessLevel;
import lombok.Getter;

/**
 * Used to build multiple changes into an entity change.
 */
public abstract class AbstractEntityChangeBuilder {
    /**
     * The change being built.
     */
    @Getter(AccessLevel.PUBLIC)
    private final EntityChangeMessage entityChangeMessage;

    protected AbstractEntityChangeBuilder(UUID userID) {
        this.entityChangeMessage = new EntityChangeMessage();
        this.entityChangeMessage.setUserId(userID);
    }

    public AbstractEntityChangeBuilder withUpdateLayout() {
        this.getEntityChangeMessage().setUpdateLayout(true);
        return this;
    }

    protected AbstractEntityChangeBuilder withEntityUpdate(Change.Entity entity, List<UUID> entityIds) {
        return withEntityUpdate(entity, entityIds, true);
    }

    protected AbstractEntityChangeBuilder withEntityUpdate(Change.Entity entity,
                                                           List<UUID> entityIds,
                                                           boolean checkIfEmpty) {
        Change change = new Change();
        change.setEntity(entity);
        change.setAction(Change.Action.UPDATE);
        change.setEntityIds(entityIds);
        return addChange(change, checkIfEmpty);
    }

    protected AbstractEntityChangeBuilder withEntityDelete(Change.Entity entity, List<UUID> entityIds) {
        return withEntityDelete(entity, entityIds, true);
    }

    protected AbstractEntityChangeBuilder withEntityDelete(Change.Entity entity,
                                                           List<UUID> entityIds,
                                                           boolean checkIfEmpty) {
        Change change = new Change();
        change.setEntity(entity);
        change.setAction(Change.Action.DELETE);
        change.setEntityIds(entityIds);
        return addChange(change, checkIfEmpty);
    }

    private AbstractEntityChangeBuilder addChange(Change change, boolean checkIfEmpty) {
        if (checkIfEmpty) {
            if (!change.getEntityIds().isEmpty()) {
                this.entityChangeMessage.addChange(change);
            }
        } else {
            this.entityChangeMessage.addChange(change);
        }
        return this;
    }
}
