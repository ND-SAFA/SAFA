package edu.nd.crc.safa.features.notifications.builders;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.notifications.entities.NotificationAction;
import edu.nd.crc.safa.features.notifications.entities.NotificationEntity;

import lombok.AccessLevel;
import lombok.Getter;

/**
 * Used to build multiple changes into an entity change.
 */
public abstract class AbstractEntityChangeBuilder<T extends AbstractEntityChangeBuilder<T>> {
    /**
     * The change being built.
     */
    @Getter(AccessLevel.PUBLIC)
    private final EntityChangeMessage entityChangeMessage;

    protected AbstractEntityChangeBuilder(UUID userID) {
        this.entityChangeMessage = new EntityChangeMessage();
        this.entityChangeMessage.setUserId(userID);
    }

    public T withUpdateLayout() {
        return withUpdateLayout(true);
    }

    public T withUpdateLayout(boolean shouldUpdate) {
        this.getEntityChangeMessage().setUpdateLayout(shouldUpdate);
        return self();
    }

    protected <EntityType extends Object> T withEntitiesUpdate(NotificationEntity entity,
                                                               List<EntityType> entities) {
        return addChange(entity, NotificationAction.UPDATE, new ArrayList<>(), entities, true);
    }

    protected T withEntityUpdate(NotificationEntity entity, List<UUID> entityIds) {
        return addChange(entity, NotificationAction.UPDATE, entityIds, new ArrayList<>(), true);
    }

    protected T withEntityUpdate(NotificationEntity entity,
                                 List<UUID> entityIds,
                                 boolean checkIfEmpty) {
        return addChange(entity, NotificationAction.UPDATE, entityIds, new ArrayList<>(), checkIfEmpty);
    }

    protected T withEntityDelete(NotificationEntity entity, List<UUID> entityIds) {
        return addChange(entity, NotificationAction.DELETE, entityIds, new ArrayList<>(), true);
    }

    private <EntityType> T addChange(NotificationEntity entity,
                                     NotificationAction action,
                                     List<UUID> entityIds,
                                     List<EntityType> entities,
                                     boolean checkIfEmpty) {
        Change change = new Change();
        change.setEntity(entity);
        change.setAction(action);
        change.setEntityIds(entityIds);
        change.setEntities(entities);
        return addChange(change, checkIfEmpty);
    }

    private T addChange(Change change, boolean checkIfEmpty) {
        if (!checkIfEmpty || !isEmpty(change)) {
            this.entityChangeMessage.addChange(change);
        }

        return self();
    }

    private boolean isEmpty(Change change) {
        return change.getEntityIds().isEmpty() && change.getEntities().isEmpty();
    }

    protected abstract T self();
}
