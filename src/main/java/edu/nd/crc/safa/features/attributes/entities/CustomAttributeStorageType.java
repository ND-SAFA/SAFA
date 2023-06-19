package edu.nd.crc.safa.features.attributes.entities;

import lombok.AllArgsConstructor;
import lombok.Getter;

/**
 * Contains details about how values for custom artifact attributes are actually
 * stored within the database.
 */
@Getter
@AllArgsConstructor
public enum CustomAttributeStorageType {

    STRING(),
    STRING_ARRAY(),
    INTEGER(),
    FLOAT(),
    BOOLEAN();
}
