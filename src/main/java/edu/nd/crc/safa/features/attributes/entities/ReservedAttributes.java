package edu.nd.crc.safa.features.attributes.entities;

import java.util.List;

public interface ReservedAttributes {

    String PREFIX = "~";

    interface Github {
        String PREFIX = ReservedAttributes.PREFIX + "gh:";

        CustomAttributeAppEntity LINK =
            new CustomAttributeAppEntity(PREFIX + "link", "Link", CustomAttributeType.TEXT);

        List<CustomAttributeAppEntity> ALL_ATTRIBUTES = List.of(LINK);
    }

    static boolean isReservedAttribute(String attributeKey) {
        return attributeKey.startsWith(PREFIX);
    }
}
