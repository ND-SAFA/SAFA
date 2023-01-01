package edu.nd.crc.safa.features.attributes.entities;

import com.fasterxml.jackson.annotation.JsonValue;
import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public enum CustomAttributeType {
    TEXT(CustomAttributeStorageType.STRING, CustomAttributeExtraInfoType.NONE),
    PARAGRAPH(CustomAttributeStorageType.STRING, CustomAttributeExtraInfoType.NONE),
    SELECT(CustomAttributeStorageType.STRING, CustomAttributeExtraInfoType.OPTIONS),
    MULTISELECT(CustomAttributeStorageType.STRING_ARRAY, CustomAttributeExtraInfoType.OPTIONS),
    RELATION(CustomAttributeStorageType.STRING_ARRAY, CustomAttributeExtraInfoType.NONE),
    DATE(CustomAttributeStorageType.STRING, CustomAttributeExtraInfoType.NONE),
    INT(CustomAttributeStorageType.INTEGER, CustomAttributeExtraInfoType.INT_BOUNDS),
    FLOAT(CustomAttributeStorageType.FLOAT, CustomAttributeExtraInfoType.FLOAT_BOUNDS),
    BOOLEAN(CustomAttributeStorageType.BOOLEAN, CustomAttributeExtraInfoType.NONE);

    private final CustomAttributeStorageType storageType;
    private final CustomAttributeExtraInfoType extraInfoType;

    @JsonValue
    public String getJsonName() {
        return name().toLowerCase();
    }
}
