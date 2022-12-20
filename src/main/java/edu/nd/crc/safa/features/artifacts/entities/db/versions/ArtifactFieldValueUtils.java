package edu.nd.crc.safa.features.artifacts.entities.db.versions;

import edu.nd.crc.safa.features.artifacts.entities.db.schema.ArtifactFieldStorageType;
import edu.nd.crc.safa.features.artifacts.entities.db.schema.ArtifactSchemaField;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

/**
 * Contains static util functions for interacting with artifact fields.
 */
public class ArtifactFieldValueUtils {

    /**
     * Saves the given string as the value of the given field within the given version
     * of the given artifact.
     *
     * @param serviceProvider Service provider - provides access to repositories.
     * @param field The schema of the field we are saving a value to.
     * @param artifactVersion The version of the artifact we are setting a value within.
     * @param value The value to set.
     */
    public static void saveArtifactValue(ServiceProvider serviceProvider, ArtifactSchemaField field,
                                         ArtifactVersion artifactVersion, String value) {

        ArtifactFieldVersion fieldVersion = new ArtifactFieldVersion();
        fieldVersion.setSchemaField(field);
        fieldVersion.setArtifactVersion(artifactVersion);
        serviceProvider.getArtifactFieldVersionRepository().save(fieldVersion);

        ArtifactFieldStorageType storageType = field.getType().getStorageType();
        if (storageType.isArrayType()) {
            for (String innerValue : unpackStringArray(value)) {
                saveArtifactValueInner(serviceProvider, storageType, innerValue, fieldVersion);
            }
        } else {
            saveArtifactValueInner(serviceProvider, storageType, value, fieldVersion);
        }
    }

    /**
     * Unpacks a string array that is encoded as a JSON string into an
     * actual string array.
     *
     * @param value JSON encoded string array
     * @return The parsed array.
     * @throws SafaError When the string is not formatted correctly.
     */
    private static String[] unpackStringArray(String value) {
        String[] values;

        try {
            values = new ObjectMapper().readValue(value, String[].class);
        } catch (JsonProcessingException e) {
            throw new SafaError(e.getMessage());
        }

        return values;
    }

    /**
     * Actually constructs and sets values in the field value object.
     * @param serviceProvider Service provider - provides access to repositories.
     * @param storageType Storage type of the field - used to get the constructor of the field type.
     * @param value The value to set.
     * @param fieldVersion The artifact field version we set a value in.
     */
    private static void saveArtifactValueInner(ServiceProvider serviceProvider, ArtifactFieldStorageType storageType, String value, ArtifactFieldVersion fieldVersion) {
        IFieldValue fieldValueObj = storageType.getFieldValueSupplier().get();
        fieldValueObj.setFieldVersion(fieldVersion);
        fieldValueObj.setValueFromString(value);
        fieldValueObj.save(serviceProvider);
    }
}
