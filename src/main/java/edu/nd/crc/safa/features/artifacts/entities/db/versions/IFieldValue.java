package edu.nd.crc.safa.features.artifacts.entities.db.versions;

import edu.nd.crc.safa.features.artifacts.services.ArtifactSystemServiceProvider;

public interface IFieldValue {
    void setFieldVersion(ArtifactFieldVersion fieldVersion);

    void setValueFromString(String strValue);

    String getValueAsString();

    void save(ArtifactSystemServiceProvider serviceProvider);
}
