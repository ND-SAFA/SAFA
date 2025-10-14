package edu.nd.crc.safa.features.attributes;

import java.util.List;

public interface ReservedAttributes {

    String PREFIX = "~";

    static boolean isReservedAttribute(String attributeKey) {
        return attributeKey.startsWith(PREFIX);
    }

    interface Github {
        String PREFIX = ReservedAttributes.PREFIX + "gh:";

        String LINK = PREFIX + "link";

        List<String> ALL_ATTRIBUTES = List.of(LINK);
    }
}
