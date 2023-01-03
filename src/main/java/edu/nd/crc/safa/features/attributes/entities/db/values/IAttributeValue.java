package edu.nd.crc.safa.features.attributes.entities.db.values;

import edu.nd.crc.safa.features.attributes.services.AttributeSystemServiceProvider;

import com.fasterxml.jackson.databind.JsonNode;

public interface IAttributeValue {
    void setAttributeVersion(ArtifactAttributeVersion attributeVersion);

    void setValueFromJsonNode(JsonNode jsonNode);

    JsonNode getValueAsJsonNode();

    void save(AttributeSystemServiceProvider serviceProvider);
}
