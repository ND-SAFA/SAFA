package services;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;

import org.json.JSONArray;
import org.json.JSONObject;

/**
 * Provides list of custom assertions.
 */
public class AssertionTestService {
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

    public void verifyTypeMessage(EntityChangeMessage message,
                                  int numberChanges,
                                  UUID typeId,
                                  Change.Entity entity,
                                  Change.Action action) {
        assertThat(message.getChanges()).hasSize(numberChanges);

        Change entityChange = message.getChangeForEntity(entity);
        assertThat(entityChange.getEntity()).isEqualTo(entity);
        assertThat(entityChange.getAction()).isEqualTo(action);
        assertThat(entityChange.getEntityIds()).hasSize(1).contains(typeId);
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
