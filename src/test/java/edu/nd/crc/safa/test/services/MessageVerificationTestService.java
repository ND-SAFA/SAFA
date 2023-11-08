package edu.nd.crc.safa.test.services;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import java.util.UUID;
import java.util.function.Function;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.documents.entities.app.DocumentAppEntity;
import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.notifications.entities.NotificationAction;
import edu.nd.crc.safa.features.notifications.entities.NotificationEntity;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.traces.entities.app.TraceAppEntity;
import edu.nd.crc.safa.features.types.entities.TypeAppEntity;

public class MessageVerificationTestService {

    public void verifyUpdateLayout(EntityChangeMessage message, boolean updateLayout) {
        assertThat(message.isUpdateLayout()).isEqualTo(updateLayout);
    }

    public void verifyTypeChange(EntityChangeMessage message,
                                 UUID entityId,
                                 NotificationAction action) {
        verifyChangeInMessage(
            message,
            entityId,
            NotificationEntity.TYPES,
            o -> ((TypeAppEntity) o).getId(),
            action
        );
    }

    public void verifyDocumentChange(EntityChangeMessage message,
                                     UUID entityId,
                                     NotificationAction action) {
        verifyChangeInMessage(
            message,
            entityId,
            NotificationEntity.DOCUMENT,
            o -> ((DocumentAppEntity) o).getDocumentId(),
            action
        );
    }

    public void verifyArtifactMessage(EntityChangeMessage message,
                                      UUID entityId,
                                      NotificationAction action) {
        verifyChangeInMessage(
            message,
            entityId,
            NotificationEntity.ARTIFACTS,
            o -> ((ArtifactAppEntity) o).getId(),
            action
        );
    }

    public void verifyTraceMessage(EntityChangeMessage message,
                                   UUID entityId,
                                   NotificationAction action) {
        verifyChangeInMessage(
            message,
            entityId,
            NotificationEntity.TRACES,
            o -> ((TraceAppEntity) o).getId(),
            action
        );
    }

    public void verifyWarningMessage(EntityChangeMessage message) {
        this.verifyChangeInMessage(message,
            null,
            NotificationEntity.WARNINGS,
            null,
            NotificationAction.UPDATE);
    }

    public void verifyProjectMessage(EntityChangeMessage message, Project project) {
        verifyChangeInMessage(message, project.getProjectId(),
            NotificationEntity.PROJECT, o -> ((Project) o).getProjectId(), NotificationAction.UPDATE);
    }

    public void verifyChangeInMessage(EntityChangeMessage message,
                                      UUID entityId,
                                      NotificationEntity entity,
                                      Function<Object, UUID> processor,
                                      NotificationAction action) {
        Change entityChange = message.getChangeForEntity(entity);
        assertThat(entityChange.getEntity()).isEqualTo(entity);
        assertThat(entityChange.getAction()).isEqualTo(action);
        if (entityId != null) {
            if (action.equals(NotificationAction.UPDATE)) {
                assertThat(entityChange.getEntities()).hasSize(1);
                List<UUID> entityIds = entityChange.getEntities().stream().map(processor).collect(Collectors.toList());
                assertThat(entityIds).contains(entityId);
            } else {
                assertThat(entityChange.getEntityIds()).hasSize(1).contains(entityId);
            }
        }
    }
}
