package edu.nd.crc.safa.utilities;

import java.util.List;
import java.util.StringJoiner;

public class StringUtil {
    /**
     * Joins elements with delimiter.
     *
     * @param elements  The string elements to join.
     * @param delimiter The delimiter used to join strings.
     * @return Single string containing all elements.
     */
    public static String join(List<String> elements, String delimiter) {
        StringJoiner joiner = new StringJoiner(delimiter);
        for (String str : elements) {
            joiner.add(str);
        }
        return joiner.toString();
    }
}
