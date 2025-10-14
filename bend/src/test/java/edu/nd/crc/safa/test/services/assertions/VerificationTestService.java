package edu.nd.crc.safa.test.services.assertions;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.function.Function;

import edu.nd.crc.safa.test.services.RetrievalTestService;
import edu.nd.crc.safa.test.services.builders.AndBuilder;
import edu.nd.crc.safa.test.services.builders.BuilderState;

import org.json.JSONArray;
import org.json.JSONObject;

/**
 * Provides list of custom assertions.
 */
public class VerificationTestService {
    private final BuilderState state;

    public VerificationTestService(BuilderState builderState) {
        this.state = builderState;
    }

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

    public <T> AndBuilder<VerificationTestService, T> notifications(Function<NotificationAssertionService, T> consumer) {
        NotificationAssertionService notificationAssertionService = new NotificationAssertionService();
        T result = consumer.apply(notificationAssertionService);
        return new AndBuilder<>(this, result, this.state);
    }
}
