package edu.nd.crc.safa.features.attributes.entities;

import lombok.AllArgsConstructor;
import lombok.Getter;

public interface ReservedAttributes {

    String PREFIX = "~";

    @AllArgsConstructor
    enum Github {

        REPO_PATH("repo_path", "Full Path"),
        LINK("link", "Link");

        private static final String PREFIX = ReservedAttributes.PREFIX + "gh:";

        private final String key;

        @Getter
        private final String displayName;

        public String getKey() {
            return PREFIX + key;
        }
    }

    static boolean isReservedAttribute(String attributeKey) {
        return attributeKey.startsWith(PREFIX);
    }
}
