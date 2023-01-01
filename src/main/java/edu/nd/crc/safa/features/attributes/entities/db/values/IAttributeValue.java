package edu.nd.crc.safa.features.attributes.entities.db.values;

import edu.nd.crc.safa.features.attributes.services.AttributeSystemServiceProvider;

public interface IAttributeValue {
    void setAttributeVersion(ArtifactAttributeVersion attributeVersion);

    void setValueFromString(String strValue);

    String getValueAsString();

    void save(AttributeSystemServiceProvider serviceProvider);
}
