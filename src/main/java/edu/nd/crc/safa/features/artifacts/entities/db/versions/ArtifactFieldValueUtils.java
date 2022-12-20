package edu.nd.crc.safa.features.artifacts.entities.db.versions;

import java.util.Optional;

import edu.nd.crc.safa.features.artifacts.entities.db.schema.ArtifactFieldStorageType;
import edu.nd.crc.safa.features.artifacts.entities.db.schema.ArtifactSchemaField;
import edu.nd.crc.safa.features.artifacts.repositories.versions.ArtifactFieldVersionRepository;
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

        ArtifactFieldVersion fieldVersion = getFieldVersion(serviceProvider, field, artifactVersion);

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
     * Gets the current field version matching the given field and artifact version, if it exists. Else
     * returns a newly constructed one.
     *
     * @param serviceProvider Service provider - provides access to repositories.
     * @param field The field object we want to access.
     * @param artifactVersion The artifact version we want to access a field for.
     * @return The field version if it existed previously, or a new one.
     */
    private static ArtifactFieldVersion getFieldVersion(ServiceProvider serviceProvider, ArtifactSchemaField field,
                                                        ArtifactVersion artifactVersion) {

        ArtifactFieldVersionRepository repo = serviceProvider.getArtifactFieldVersionRepository();

        Optional<ArtifactFieldVersion> foundFieldVersion =
            repo.findByArtifactVersionAndSchemaField(artifactVersion, field);

        return foundFieldVersion.orElseGet(() -> {
            ArtifactFieldVersion fieldVersion = new ArtifactFieldVersion();
            fieldVersion.setArtifactVersion(artifactVersion);
            fieldVersion.setSchemaField(field);
            repo.save(fieldVersion);
            return fieldVersion;
        });
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
    private static void saveArtifactValueInner(ServiceProvider serviceProvider, ArtifactFieldStorageType storageType,
                                               String value, ArtifactFieldVersion fieldVersion) {

        IFieldValue fieldValueObj = storageType.getFieldValueSupplier().get();
        fieldValueObj.setFieldVersion(fieldVersion);
        fieldValueObj.setValueFromString(value);
        fieldValueObj.save(serviceProvider);
    }
}
