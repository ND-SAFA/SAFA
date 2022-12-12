package edu.nd.crc.safa.features.artifacts.entities;

import edu.nd.crc.safa.features.artifacts.entities.db.schema.ArtifactFieldExtraInfoType;
import edu.nd.crc.safa.features.artifacts.entities.db.schema.ArtifactFieldStorageType;

public enum ArtifactFieldType {
    TEXT(ArtifactFieldStorageType.STRING, ArtifactFieldExtraInfoType.NONE),
    PARAGRAPH(ArtifactFieldStorageType.STRING, ArtifactFieldExtraInfoType.NONE),
    SELECT(ArtifactFieldStorageType.STRING, ArtifactFieldExtraInfoType.OPTIONS),
    MULTISELECT(ArtifactFieldStorageType.STRING_ARRAY, ArtifactFieldExtraInfoType.OPTIONS),
    RELATION(ArtifactFieldStorageType.STRING_ARRAY, ArtifactFieldExtraInfoType.NONE),
    DATE(ArtifactFieldStorageType.STRING, ArtifactFieldExtraInfoType.NONE),
    INT(ArtifactFieldStorageType.INTEGER, ArtifactFieldExtraInfoType.INT_BOUNDS),
    FLOAT(ArtifactFieldStorageType.FLOAT, ArtifactFieldExtraInfoType.FLOAT_BOUNDS),
    BOOLEAN(ArtifactFieldStorageType.BOOLEAN, ArtifactFieldExtraInfoType.NONE);

    private final ArtifactFieldStorageType storageType;
    private final ArtifactFieldExtraInfoType extraInfoType;

    ArtifactFieldType(ArtifactFieldStorageType storageType, ArtifactFieldExtraInfoType extraInfoType) {
        this.storageType = storageType;
        this.extraInfoType = extraInfoType;
    }

    public ArtifactFieldStorageType getStorageType() {
        return storageType;
    }

    public ArtifactFieldExtraInfoType getExtraInfoType() {
        return extraInfoType;
    }
}
