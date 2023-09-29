package edu.nd.crc.safa.test.services;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.notifications.entities.NotificationAction;
import edu.nd.crc.safa.features.notifications.entities.NotificationEntity;
import edu.nd.crc.safa.features.traces.entities.app.TraceMatrixAppEntity;
import edu.nd.crc.safa.features.types.entities.db.ArtifactType;
import edu.nd.crc.safa.features.users.entities.IUser;
import edu.nd.crc.safa.features.users.entities.app.UserAppEntity;
import edu.nd.crc.safa.test.services.notifications.NotificationTestService;

import org.json.JSONArray;
import org.json.JSONObject;

/**
 * Provides list of custom assertions.
 */
public class AssertionTestService {
    public void verifyArtifactInDelta(RetrievalTestService retrievalService,
                                      String projectName,
                                      JSONObject artifactDelta,
                                      String deltaName,
                                      String artifactName) {
        String artifactId = retrievalService.getId(projectName, artifactName);
        assertThat(artifactDelta.getJSONObject(deltaName).has(artifactId)).isTrue();
    }

    public void verifyNumOfChangesInDelta(JSONObject entityDelta,
                                          String deltaName,
                                          int expected) {
        String assertionTitle = String.format("# of entities %s", deltaName);
        int nTracesAdded = entityDelta.getJSONObject(deltaName).keySet().toArray().length;
        assertThat(nTracesAdded).as(assertionTitle).isEqualTo(expected);
    }

    public void assertMatch(Object expected, Object actual) {
        if (expected instanceof JSONObject) {
            assertObjectsMatch((JSONObject) expected, (JSONObject) actual);
        } else if (expected instanceof JSONArray) {
            assertArraysMatch((JSONArray) expected, (JSONArray) actual);
        } else {
            assertThat(actual).isEqualTo(expected);
        }
    }

    public void assertObjectsMatch(JSONObject expected, JSONObject actual) {
        assertObjectsMatch(expected, actual, new ArrayList<>());
    }

    public void assertObjectsMatch(JSONObject expected,
                                   JSONObject actual,
                                   List<String> ignoreProperties) {
        for (Iterator<String> expectedIterator = expected.keys(); expectedIterator.hasNext(); ) {
            String key = expectedIterator.next();
            if (ignoreProperties.contains(key)) {
                continue;
            }

            if (!actual.has(key)) {
                throw new RuntimeException(actual + " does not contain key:" + key);
            }

            Object expectedValue = expected.get(key);
            Object actualValue = actual.get(key);

            assertMatch(expectedValue, actualValue);
        }
    }

    public void assertArraysMatch(JSONArray expected, JSONArray actual) {
        assertThat(actual.length()).isEqualTo(expected.length());
        for (int i = 0; i < expected.length(); i++) {
            Object expectedValue = expected.get(i);
            Object actualValue = actual.get(i);
            assertMatch(expectedValue, actualValue);
        }
    }

    public void verifyActiveMembers(List<IUser> users, NotificationTestService notificationTestService) throws Exception {
        IUser coreUser = users.get(0);
        EntityChangeMessage message = notificationTestService.getEntityMessage(coreUser);
        verifyActiveMembers(users, message);
    }


    public void verifyArtifactTypeMessage(EntityChangeMessage message, String artifactTypeName) {
        ArtifactType artifactType =
            (ArtifactType) verifySingleEntityChanges(message,
                List.of(NotificationEntity.TYPES),
                List.of(1)).get(0);
        assertThat(artifactType.getName()).isEqualTo(artifactTypeName);
    }

    public void verifyTraceMatrixMessage(EntityChangeMessage message, List<String> types) {
        String childType = types.get(0);
        String parentType = types.get(1);
        TraceMatrixAppEntity traceMatrix = (TraceMatrixAppEntity) verifySingleEntityChanges(
            message,
            List.of(NotificationEntity.TRACE_MATRICES),
            List.of(1)).get(0);
        assertThat(traceMatrix.getSourceType()).isEqualTo(childType);
        assertThat(traceMatrix.getTargetType()).isEqualTo(parentType);
    }

    public void verifyProjectEntitiesMessage(EntityChangeMessage message, int nArtifacts, int nTraces) {
        assertThat(message.getChanges()).hasSize(2);
        Change artifactChange = message.getChanges().get(0);

        assertThat(artifactChange.getEntity()).isEqualTo(NotificationEntity.ARTIFACTS);
        assertThat(artifactChange.getEntities()).hasSize(nArtifacts);

        Change traceChange = message.getChanges().get(1);
        assertThat(traceChange.getEntity()).isEqualTo(NotificationEntity.TRACES);
        assertThat(traceChange.getEntities()).hasSize(nTraces);
    }

    public List<Object> verifySingleEntityChanges(EntityChangeMessage message,
                                                  List<NotificationEntity> entities,
                                                  List<Integer> nEntities) {
        assertThat(message.getChanges()).hasSize(entities.size());
        List<Object> objects = new ArrayList<>();
        for (int i = 0; i < entities.size(); i++) {
            int nEntitiesExpected = nEntities.get(i);
            NotificationEntity entity = entities.get(i);
            Change change = message.getChanges().get(i);
            assertThat(change.getEntity()).isEqualTo(entity);
            assertThat(change.getEntities()).hasSize(nEntitiesExpected);
            assertThat(change.getAction()).isEqualTo(NotificationAction.UPDATE);
            objects.addAll(change.getEntities());
        }

        return objects;
    }

    private void verifyActiveMembers(List<IUser> users, EntityChangeMessage message) throws Exception {
        List<Change> changes = message.getChanges();
        assertThat(changes).hasSize(1);
        Change change = changes.get(0);
        assertThat(change.getEntity()).isEqualTo(NotificationEntity.ACTIVE_MEMBERS);
        assertThat(change.getEntities()).hasSize(users.size());
        List<UUID> activeUsers = change.getEntities()
            .stream()
            .map(u -> (UserAppEntity) u)
            .map(UserAppEntity::getUserId)
            .sorted() // sorting to guarantee order in both expected and resulting.
            .collect(Collectors.toList());
        List<UUID> expectedUsers = users.stream().map(IUser::getUserId).sorted().collect(Collectors.toList());
        assertThat(activeUsers).isEqualTo(expectedUsers);
    }
}
