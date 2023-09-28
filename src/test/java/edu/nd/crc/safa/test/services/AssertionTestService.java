package edu.nd.crc.safa.test.services;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.users.entities.app.UserAppEntity;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

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

    public void verifyOnlyActiveMember(SafaUser user, EntityChangeMessage message) throws Exception {
        List<Change> changes = message.getChanges();
        assertThat(changes).hasSize(1);
        Change change = changes.get(0);
        assertThat(change.getEntity()).isEqualTo(Change.Entity.ACTIVE_MEMBERS);
        assertThat(change.getEntities()).hasSize(1);
        UserAppEntity messageUser = (UserAppEntity) change.getEntities().get(0);
        assertThat(messageUser.getUserId()).isEqualTo(user.getUserId());
    }
}
