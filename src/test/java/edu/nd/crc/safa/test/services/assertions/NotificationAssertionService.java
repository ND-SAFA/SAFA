package edu.nd.crc.safa.test.services.assertions;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.UUID;
import java.util.function.BiConsumer;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.notifications.entities.NotificationAction;
import edu.nd.crc.safa.features.notifications.entities.NotificationEntity;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.traces.entities.app.TraceMatrixAppEntity;
import edu.nd.crc.safa.features.types.entities.TypeAppEntity;
import edu.nd.crc.safa.features.users.entities.IUser;
import edu.nd.crc.safa.features.users.entities.app.UserAppEntity;
import edu.nd.crc.safa.test.services.notifications.NotificationTestService;

public class NotificationAssertionService {
    public NotificationAssertionService verifyMemberNotification(EntityChangeMessage memberNotification,
                                                                 List<String> emails) {
        assertEquals(1, memberNotification.getChanges().size());
        Change change = memberNotification.getChanges().get(0);
        List<String> projectMembers = change
            .getEntities()
            .stream()
            .map(a -> (UserAppEntity) a)
            .map(UserAppEntity::getEmail)
            .collect(Collectors.toList());

        assertEquals(new HashSet<>(emails), new HashSet<>(projectMembers));
        return this;
    }

    @Deprecated()
    public NotificationAssertionService verifyActiveMembers(List<IUser> users, NotificationTestService notificationTestService) {
        IUser coreUser = users.get(0);
        EntityChangeMessage message = notificationTestService.getEntityMessage(coreUser);
        verifyActiveMembers(users, message);
        return this;
    }

    public NotificationAssertionService verifyProjectMessage(EntityChangeMessage message) {
        return verifyMessage(message,
            List.of(NotificationEntity.PROJECT),
            List.of(NotificationAction.UPDATE),
            (a, b) -> {
                if (!b.isEmpty()) {
                    throw new RuntimeException("Expected no entities to be included"); // should not contain
                }
            });
    }


    public NotificationAssertionService verifyArtifactTypeMessage(EntityChangeMessage message, String artifactTypeName) {
        TypeAppEntity artifactType =
            (TypeAppEntity) verifySingleEntityChanges(message,
                List.of(NotificationEntity.TYPES),
                List.of(1)).get(0);
        assertThat(artifactType.getName()).isEqualTo(artifactTypeName);
        return this;
    }

    public NotificationAssertionService verifyTraceMatrixMessage(EntityChangeMessage message, List<String> types) {
        String childType = types.get(0);
        String parentType = types.get(1);
        TraceMatrixAppEntity traceMatrix = (TraceMatrixAppEntity) verifySingleEntityChanges(
            message,
            List.of(NotificationEntity.TRACE_MATRICES),
            List.of(1)).get(0);
        assertThat(traceMatrix.getSourceType()).isEqualTo(childType);
        assertThat(traceMatrix.getTargetType()).isEqualTo(parentType);
        return this;
    }

    public NotificationAssertionService verifyProjectEntitiesMessage(EntityChangeMessage message, int nArtifacts, int nTraces) {
        assertThat(message.getChanges()).hasSize(2);
        Change artifactChange = message.getChanges().get(0);

        assertThat(artifactChange.getEntity()).isEqualTo(NotificationEntity.ARTIFACTS);
        assertThat(artifactChange.getEntities()).hasSize(nArtifacts);

        Change traceChange = message.getChanges().get(1);
        assertThat(traceChange.getEntity()).isEqualTo(NotificationEntity.TRACES);
        assertThat(traceChange.getEntities()).hasSize(nTraces);
        return this;
    }

    public List<Object> verifySingleEntityChanges(EntityChangeMessage message,
                                                  List<NotificationEntity> entities,
                                                  List<Integer> nEntities) {
        List<Object> objects = new ArrayList<>();
        List<NotificationAction> actions = entities.stream().map(e -> NotificationAction.UPDATE).collect(Collectors.toList());

        verifyMessage(message,
            entities,
            actions,
            (i, e) -> {
                assertThat(e).hasSize(nEntities.get(i));
                objects.addAll(e);
            });
        return objects;
    }

    private void verifyActiveMembers(List<IUser> users, EntityChangeMessage message) {
        List<UUID> expectedUsers = users.stream().map(IUser::getUserId).sorted().collect(Collectors.toList());
        verifyMessage(message,
            List.of(NotificationEntity.ACTIVE_MEMBERS),
            List.of(NotificationAction.UPDATE),
            (i, activeUsers) -> assertThat(activeUsers).isEqualTo(expectedUsers));
    }

    public NotificationAssertionService verifyMessage(EntityChangeMessage message,
                                                      List<NotificationEntity> entities,
                                                      List<NotificationAction> actions,
                                                      BiConsumer<Integer, List<Object>> verifier) {
        if (entities.size() != actions.size()) {
            String error = String.format("Entities (%s) does not match actions (%s).", entities.size(), actions.size());
            throw new SafaError(error);
        }
        int nChanges = entities.size();
        assertThat(message.getChanges()).hasSize(nChanges);
        for (int i = 0; i < nChanges; i++) {
            NotificationEntity entity = entities.get(i);
            NotificationAction action = actions.get(i);
            Change change = message.getChanges().get(i);
            assertThat(change.getAction()).isEqualTo(action);
            assertThat(change.getEntity()).isEqualTo(entity);
            verifier.accept(i, change.getEntities());
        }
        return this;
    }

    public NotificationAssertionService verifyDocumentChangeMessage(EntityChangeMessage message) {
        this.verifyMessage(message,
            List.of(NotificationEntity.DOCUMENT, NotificationEntity.ARTIFACTS),
            List.of(NotificationAction.UPDATE, NotificationAction.UPDATE),
            (i, e) -> {
                assertThat(e.size()).isEqualTo(1);
            });
        return this;
    }
}
