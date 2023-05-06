package edu.nd.crc.safa.features.attributes.entities;

import java.util.List;

public interface ReservedAttributes {

    String PREFIX = "~";

    interface Github {
        String PREFIX = ReservedAttributes.PREFIX + "gh:";

        CustomAttributeAppEntity REPO_PATH =
            new CustomAttributeAppEntity(PREFIX + "repo_path", "Full Path", CustomAttributeType.TEXT);
        CustomAttributeAppEntity LINK =
            new CustomAttributeAppEntity(PREFIX + "link", "Link", CustomAttributeType.TEXT);

        List<CustomAttributeAppEntity> ALL_ATTRIBUTES = List.of(REPO_PATH, LINK);
    }

    static boolean isReservedAttribute(String attributeKey) {
        return attributeKey.startsWith(PREFIX);
    }
}
