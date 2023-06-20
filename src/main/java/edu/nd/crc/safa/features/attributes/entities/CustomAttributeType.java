package edu.nd.crc.safa.features.attributes.entities;

import com.fasterxml.jackson.annotation.JsonValue;
import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public enum CustomAttributeType {
    TEXT(CustomAttributeExtraInfoType.NONE),
    PARAGRAPH(CustomAttributeExtraInfoType.NONE),
    SELECT(CustomAttributeExtraInfoType.OPTIONS),
    MULTISELECT(CustomAttributeExtraInfoType.OPTIONS),
    RELATION(CustomAttributeExtraInfoType.NONE),
    DATE(CustomAttributeExtraInfoType.NONE),
    INT(CustomAttributeExtraInfoType.INT_BOUNDS),
    FLOAT(CustomAttributeExtraInfoType.FLOAT_BOUNDS),
    BOOLEAN(CustomAttributeExtraInfoType.NONE);

    private final CustomAttributeExtraInfoType extraInfoType;

    @JsonValue
    public String getJsonName() {
        return name().toLowerCase();
    }
}
