package unit;

import com.fasterxml.jackson.databind.ObjectMapper;

/**
 * Responsible for holding any response/request parsing functions.
 */
public class TestUtil {
    public static String asJsonString(final Object obj) {
        try {
            return new ObjectMapper().writeValueAsString(obj);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}
