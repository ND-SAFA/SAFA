package edu.nd.crc.safa.features.artifacts.entities.db.schema;

import java.util.List;
import java.util.function.BiFunction;
import java.util.function.Supplier;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.db.versions.ArtifactFieldVersion;
import edu.nd.crc.safa.features.artifacts.entities.db.versions.BooleanFieldValue;
import edu.nd.crc.safa.features.artifacts.entities.db.versions.FloatFieldValue;
import edu.nd.crc.safa.features.artifacts.entities.db.versions.IFieldValue;
import edu.nd.crc.safa.features.artifacts.entities.db.versions.IntegerFieldValue;
import edu.nd.crc.safa.features.artifacts.entities.db.versions.StringArrayFieldValue;
import edu.nd.crc.safa.features.artifacts.entities.db.versions.StringFieldValue;
import edu.nd.crc.safa.features.artifacts.services.ArtifactSystemServiceProvider;

import lombok.AllArgsConstructor;
import lombok.Getter;

/**
 * Contains details about how values for custom artifact attributes are actually
 * stored within the database.
 */
@Getter
@AllArgsConstructor
public enum ArtifactFieldStorageType {

    STRING(StringFieldValue::new, false,
        (serviceProvider, artifactFieldVersion) ->
            serviceProvider.getStringFieldValueRepository().getByFieldVersion(artifactFieldVersion)
                .map(StringFieldValue::getValueAsString).orElse(null)),
    STRING_ARRAY(StringArrayFieldValue::new, true,
        (serviceProvider, artifactFieldVersion) ->
            toJsonString(serviceProvider.getStringArrayFieldValueRepository().getByFieldVersion(artifactFieldVersion))),
    INTEGER(IntegerFieldValue::new, false,
        (serviceProvider, artifactFieldVersion) ->
            serviceProvider.getIntegerFieldValueRepository().getByFieldVersion(artifactFieldVersion)
                .map(IntegerFieldValue::getValueAsString).orElse(null)),
    FLOAT(FloatFieldValue::new, false,
        (serviceProvider, artifactFieldVersion) ->
            serviceProvider.getFloatFieldValueRepository().getByFieldVersion(artifactFieldVersion)
                .map(FloatFieldValue::getValueAsString).orElse(null)),
    BOOLEAN(BooleanFieldValue::new, false,
        (serviceProvider, artifactFieldVersion) ->
            serviceProvider.getBooleanFieldValueRepository().getByFieldVersion(artifactFieldVersion)
                .map(BooleanFieldValue::getValueAsString).orElse(null));

    final Supplier<IFieldValue> fieldValueConstructor;
    final boolean isArrayType;
    final BiFunction<ArtifactSystemServiceProvider, ArtifactFieldVersion, String> stringValueRetriever;

    private static String toJsonString(List<StringArrayFieldValue> stringArrayFieldValues) {
        return stringArrayFieldValues.stream()
            .map(StringArrayFieldValue::getValueAsString)
            .collect(Collectors.joining(",", "[", "]'"));
    }
}
