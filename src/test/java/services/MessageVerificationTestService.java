package services;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.UUID;

import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;

public class MessageVerificationTestService {

    public void verifyUpdateLayout(EntityChangeMessage message, boolean updateLayout) {
        assertThat(message.isUpdateLayout()).isEqualTo(updateLayout);
    }

    public void verifyTypeChange(EntityChangeMessage message,
                                 UUID entityId,
                                 Change.Action action) {
        verifyChangeInMessage(
            message,
            entityId,
            Change.Entity.TYPES,
            action
        );
    }

    public void verifyDocumentChange(EntityChangeMessage message,
                                     UUID entityId,
                                     Change.Action action) {
        verifyChangeInMessage(
            message,
            entityId,
            Change.Entity.DOCUMENT,
            action
        );
    }

    public void verifyArtifactMessage(EntityChangeMessage message,
                                      UUID entityId,
                                      Change.Action action) {
        verifyChangeInMessage(
            message,
            entityId,
            Change.Entity.ARTIFACTS,
            action
        );
    }

    public void verifyTraceMessage(EntityChangeMessage message,
                                   UUID entityId,
                                   Change.Action action) {
        verifyChangeInMessage(
            message,
            entityId,
            Change.Entity.TRACES,
            action
        );
    }

    public void verifyWarningMessage(EntityChangeMessage message) {
        this.verifyChangeInMessage(message,
            null,
            Change.Entity.WARNINGS,
            Change.Action.UPDATE);
    }

    public void verifyChangeInMessage(EntityChangeMessage message,
                                      UUID typeId,
                                      Change.Entity entity,
                                      Change.Action action) {
        Change entityChange = message.getChangeForEntity(entity);
        assertThat(entityChange.getEntity()).isEqualTo(entity);
        assertThat(entityChange.getAction()).isEqualTo(action);
        if (typeId != null) {
            assertThat(entityChange.getEntityIds()).hasSize(1).contains(typeId);
        }
    }
}
