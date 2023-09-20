package edu.nd.crc.safa.utilities;

import java.util.Objects;

import edu.nd.crc.safa.features.projects.entities.app.SafaError;

public interface AssertUtils {
    static void assertThat(boolean value, String message) {
        if (!value) {
            throw new SafaError(message);
        }
    }

    static void assertNull(Object object, String message) {
        assertThat(object == null, message);
    }

    static void assertNotNull(Object object, String message) {
        assertThat(object != null, message);
    }

    static void assertEqual(Object object1, Object object2, String message) {
        assertThat(Objects.equals(object1, object2), message);
    }

    static void assertNotEquals(Object object1, Object object2, String message) {
        assertThat(!Objects.equals(object1, object2), message);
    }
}
