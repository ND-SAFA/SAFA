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

/**
 * Contains details about how values for custom artifact attributes are actually
 * stored within the database.
 */
@Getter
@AllArgsConstructor
public enum CustomAttributeStorageType {

    STRING(StringAttributeValue::new, false,
        (serviceProvider, artifactAttributeVersion) ->
            serviceProvider.getStringAttributeValueRepository().getByAttributeVersion(artifactAttributeVersion)
                .map(StringAttributeValue::getValueAsJsonNode).orElse(null)),
    STRING_ARRAY(StringArrayAttributeValue::new, true,
        (serviceProvider, artifactAttributeVersion) ->
            toJsonArray(serviceProvider.getStringArrayAttributeValueRepository()
                    .getByAttributeVersion(artifactAttributeVersion))),
    INTEGER(IntegerAttributeValue::new, false,
        (serviceProvider, artifactAttributeVersion) ->
            serviceProvider.getIntegerAttributeValueRepository().getByAttributeVersion(artifactAttributeVersion)
                .map(IntegerAttributeValue::getValueAsJsonNode).orElse(null)),
    FLOAT(FloatAttributeValue::new, false,
        (serviceProvider, artifactAttributeVersion) ->
            serviceProvider.getFloatAttributeValueRepository().getByAttributeVersion(artifactAttributeVersion)
                .map(FloatAttributeValue::getValueAsJsonNode).orElse(null)),
    BOOLEAN(BooleanAttributeValue::new, false,
        (serviceProvider, artifactAttributeVersion) ->
            serviceProvider.getBooleanAttributeValueRepository().getByAttributeVersion(artifactAttributeVersion)
                .map(BooleanAttributeValue::getValueAsJsonNode).orElse(null));

    final Supplier<IAttributeValue> attributeValueConstructor;
    final boolean isArrayType;
    final BiFunction<AttributeSystemServiceProvider, ArtifactAttributeVersion, JsonNode> jsonValueRetriever;

    private static JsonNode toJsonArray(List<StringArrayAttributeValue> stringArrayAttributeValues) {
        List<JsonNode> childNodes = stringArrayAttributeValues
                .stream()
                .map(StringArrayAttributeValue::getValueAsJsonNode)
                .collect(Collectors.toList());

        return new ArrayNode(JsonNodeFactory.instance, childNodes);
    }
}
