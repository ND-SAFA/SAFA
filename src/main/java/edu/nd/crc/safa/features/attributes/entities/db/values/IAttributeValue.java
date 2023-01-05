package edu.nd.crc.safa.features.attributes.entities.db.values;

import edu.nd.crc.safa.features.attributes.services.AttributeSystemServiceProvider;

import com.fasterxml.jackson.databind.JsonNode;

/**
 * This is an interface implemented by all possible storage types for custom
 * attributes. Mostly, it facilitates converting between these database
 * representations and json, as well as saving values to the correct repositories.
 */
public interface IAttributeValue {

    /**
     * Sets the attribute version this value is associated with. Each attribute
     * version creates the link between an artifact version and a custom attribute
     * so that custom attributes can be versioned just like all other attributes.
     *
     * @param attributeVersion The attribute version for this value.
     */
    void setAttributeVersion(ArtifactAttributeVersion attributeVersion);

    /**
     * Set the value of this attribute from a json node.
     *
     * @param jsonNode The json node containing the json encoded representation of
     *                 the value of this attribute.
     */
    void setValueFromJsonNode(JsonNode jsonNode);

    /**
     * Gets the value of this attribute as a json node which can then be give directly
     * to Jackson for serialization.
     *
     * @return The value from this object as a json node.
     */
    JsonNode getValueAsJsonNode();

    /**
     * Saves this value into the database. Implementations of this function should check
     * if there is already a value associated with this artifact version before saving and
     * make sure to set the ID appropriately so that the value is overwritten rather than
     * creating a new value. This does not apply to array types, as the old values are cleared
     * before the new ones are saved.
     *
     * @param serviceProvider The service provider - gives access to the repositories.
     */
    void save(AttributeSystemServiceProvider serviceProvider);
}
