package edu.nd.crc.safa.features.attributes.entities;

import java.util.List;
import java.util.function.BiFunction;
import java.util.function.Supplier;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.attributes.entities.db.values.ArtifactAttributeVersion;
import edu.nd.crc.safa.features.attributes.entities.db.values.BooleanAttributeValue;
import edu.nd.crc.safa.features.attributes.entities.db.values.FloatAttributeValue;
import edu.nd.crc.safa.features.attributes.entities.db.values.IAttributeValue;
import edu.nd.crc.safa.features.attributes.entities.db.values.IntegerAttributeValue;
import edu.nd.crc.safa.features.attributes.entities.db.values.StringArrayAttributeValue;
import edu.nd.crc.safa.features.attributes.entities.db.values.StringAttributeValue;
import edu.nd.crc.safa.features.attributes.services.AttributeSystemServiceProvider;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.JsonNodeFactory;
import lombok.AllArgsConstructor;
import lombok.Getter;
import org.springframework.data.domain.Sort;

/**
 * Contains details about how values for custom artifact attributes are actually
 * stored within the database.
 */
@Getter
@AllArgsConstructor
public enum CustomAttributeStorageType {

    STRING(StringAttributeValue::new, false, CustomAttributeStorageType::stringJsonValueRetriever),
    STRING_ARRAY(StringArrayAttributeValue::new, true, CustomAttributeStorageType::stringArrayJsonValueRetriever),
    INTEGER(IntegerAttributeValue::new, false, CustomAttributeStorageType::integerJsonValueRetriever),
    FLOAT(FloatAttributeValue::new, false, CustomAttributeStorageType::floatJsonValueRetriever),
    BOOLEAN(BooleanAttributeValue::new, false, CustomAttributeStorageType::boolJsonValueRetriever);

    final Supplier<IAttributeValue> attributeValueConstructor;
    final boolean isArrayType;
    final BiFunction<AttributeSystemServiceProvider, ArtifactAttributeVersion, JsonNode> jsonValueRetriever;

    /**
     * Converts a list of attribute values to a json array node.
     *
     * @param attributeValues List of attribute values to put into a json array.
     * @return A json array node containing the given values.
     */
    private static JsonNode toJsonArray(List<? extends IAttributeValue> attributeValues) {
        List<JsonNode> childNodes = attributeValues
                .stream()
                .map(IAttributeValue::getValueAsJsonNode)
                .collect(Collectors.toList());

        return new ArrayNode(JsonNodeFactory.instance, childNodes);
    }

    /**
     * Retrieves a string attribute value as a json node.
     *
     * @param serviceProvider The service provider (gives access to repos).
     * @param attributeVersion The attribute version to fetch.
     * @return A json node with the string value inside of it.
     */
    private static JsonNode stringJsonValueRetriever(AttributeSystemServiceProvider serviceProvider,
                                                     ArtifactAttributeVersion attributeVersion) {
        return serviceProvider.getStringAttributeValueRepository()
                .getByAttributeVersion(attributeVersion)
                .map(StringAttributeValue::getValueAsJsonNode)
                .orElse(null);
    }

    /**
     * Retrieves a string array attribute value as a json node.
     *
     * @param serviceProvider The service provider (gives access to repos).
     * @param attributeVersion The attribute version to fetch.
     * @return A json node with the string array value inside of it.
     */
    private static JsonNode stringArrayJsonValueRetriever(AttributeSystemServiceProvider serviceProvider,
                                                          ArtifactAttributeVersion attributeVersion) {
        List<StringArrayAttributeValue> stringArrayAttributeValues =
                serviceProvider.getStringArrayAttributeValueRepository()
                        .getByAttributeVersion(attributeVersion, Sort.by("value"));
        return toJsonArray(stringArrayAttributeValues);
    }

    /**
     * Retrieves an integer attribute value as a json node.
     *
     * @param serviceProvider The service provider (gives access to repos).
     * @param attributeVersion The attribute version to fetch.
     * @return A json node with the integer value inside of it.
     */
    private static JsonNode integerJsonValueRetriever(AttributeSystemServiceProvider serviceProvider,
                                                      ArtifactAttributeVersion attributeVersion) {
        return serviceProvider.getIntegerAttributeValueRepository()
                .getByAttributeVersion(attributeVersion)
                .map(IntegerAttributeValue::getValueAsJsonNode)
                .orElse(null);
    }

    /**
     * Retrieves a float attribute value as a json node.
     *
     * @param serviceProvider The service provider (gives access to repos).
     * @param attributeVersion The attribute version to fetch.
     * @return A json node with the float value inside of it.
     */
    private static JsonNode floatJsonValueRetriever(AttributeSystemServiceProvider serviceProvider,
                                                    ArtifactAttributeVersion attributeVersion) {
        return serviceProvider.getFloatAttributeValueRepository()
                .getByAttributeVersion(attributeVersion)
                .map(FloatAttributeValue::getValueAsJsonNode)
                .orElse(null);
    }

    /**
     * Retrieves a boolean attribute value as a json node.
     *
     * @param serviceProvider The service provider (gives access to repos).
     * @param attributeVersion The attribute version to fetch.
     * @return A json node with the boolean value inside of it.
     */
    private static JsonNode boolJsonValueRetriever(AttributeSystemServiceProvider serviceProvider,
                                                   ArtifactAttributeVersion attributeVersion) {
        return serviceProvider.getBooleanAttributeValueRepository()
                .getByAttributeVersion(attributeVersion)
                .map(BooleanAttributeValue::getValueAsJsonNode)
                .orElse(null);
    }
}
