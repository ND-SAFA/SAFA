package edu.nd.crc.safa.features.artifacts.services;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import javax.transaction.Transactional;

import edu.nd.crc.safa.features.artifacts.entities.db.schema.ArtifactFieldStorageType;
import edu.nd.crc.safa.features.artifacts.entities.db.schema.CustomAttribute;
import edu.nd.crc.safa.features.artifacts.entities.db.versions.ArtifactFieldVersion;
import edu.nd.crc.safa.features.artifacts.entities.db.versions.ArtifactVersion;
import edu.nd.crc.safa.features.artifacts.entities.db.versions.IFieldValue;
import edu.nd.crc.safa.features.artifacts.repositories.versions.ArtifactFieldVersionRepository;
import edu.nd.crc.safa.features.artifacts.repositories.versions.ArtifactVersionRepositoryImpl;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

/**
 * Contains util functions for interacting with artifact fields.
 */
@Service
public class ArtifactFieldValueService {

    private final ArtifactSystemServiceProvider serviceProvider;

    private final Logger logger = LoggerFactory.getLogger(ArtifactVersionRepositoryImpl.class);

    public ArtifactFieldValueService(ArtifactSystemServiceProvider serviceProvider) {
        this.serviceProvider = serviceProvider;
    }

    /**
     * Gets a map with all the custom attributes that are set for this artifact. The map
     * goes from keyname to string value.
     *
     * @param artifactVersion The artifact version we're looking at.
     * @return A map from field keynames to values.
     */
    public Map<String, String> getCustomAttributeValuesForArtifact(ArtifactVersion artifactVersion) {

        List<ArtifactFieldVersion> fieldVersions =
            serviceProvider.getArtifactFieldVersionRepository().findByArtifactVersion(artifactVersion);

        Map<String, String> out = new HashMap<>();

        for (ArtifactFieldVersion fieldVersion : fieldVersions) {
            String fieldValue = fieldVersion.getValueType().getStringValueRetriever()
                .apply(serviceProvider, fieldVersion);

            out.put(fieldVersion.getSchemaField().getKeyname(), fieldValue);
        }

        return out;
    }

    /**
     * Saves the given string as the value of the given field within the given version
     * of the given artifact.
     *
     * @param field The schema of the field we are saving a value to.
     * @param artifactVersion The version of the artifact we are setting a value within.
     * @param value The value to set.
     */
    @Transactional
    public void saveAttributeValue(CustomAttribute field, ArtifactVersion artifactVersion, String value) {

        ArtifactFieldVersion fieldVersion = getFieldVersion(field, artifactVersion);

        ArtifactFieldStorageType storageType = field.getType().getStorageType();
        if (storageType.isArrayType()) {
            clearArrayTypeValues(fieldVersion);
            for (String innerValue : unpackStringArray(value)) {
                saveArtifactValueInner(storageType, innerValue, fieldVersion);
            }
        } else {
            saveArtifactValueInner(storageType, value, fieldVersion);
        }
    }

    /**
     * The save function of regular types is expected to overwrite the old value if one exists, but
     * for an array, that doesn't really work, so this function clears out the old values before we
     * write the new values to the database.
     *
     * @param fieldVersion The field version we're writing to.
     */
    private void clearArrayTypeValues(ArtifactFieldVersion fieldVersion) {
        ArtifactFieldStorageType storageType = fieldVersion.getSchemaField().getType().getStorageType();
        switch (storageType) {
            case STRING_ARRAY:
                serviceProvider.getStringArrayFieldValueRepository().deleteByFieldVersion(fieldVersion);
                break;
            default:
                logger.error("Unhandled array type: " + storageType);
                break;
        }
    }

    /**
     * Saves the given strings as the values of the given fields within the given version
     * of the given artifact.
     *
     * @param artifactVersion The version of the artifact we are setting a value within.
     * @param attributeValues The values to set.
     */
    @Transactional
    public void saveAllAttributeValues(ArtifactVersion artifactVersion, Map<String, String> attributeValues) {

        for (Map.Entry<String, String> entry : attributeValues.entrySet()) {
            String key = entry.getKey();
            String value = entry.getValue();

            Optional<CustomAttribute> attribute =
                serviceProvider.getCustomAttributeRepository()
                    .findByProjectAndKeyname(artifactVersion.getArtifact().getProject(), key);

            if (attribute.isPresent()) {
                saveAttributeValue(attribute.get(), artifactVersion, value);
            } else {
                logger.warn("Attempting to save a value for an unknown attribute: " + key);
            }
        }
    }

    /**
     * Gets the current field version matching the given field and artifact version, if it exists. Else
     * returns a newly constructed one.
     *
     * @param field The field object we want to access.
     * @param artifactVersion The artifact version we want to access a field for.
     * @return The field version if it existed previously, or a new one.
     */
    private ArtifactFieldVersion getFieldVersion(CustomAttribute field, ArtifactVersion artifactVersion) {

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
    private String[] unpackStringArray(String value) {
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
     * @param storageType Storage type of the field - used to get the constructor of the field type.
     * @param value The value to set.
     * @param fieldVersion The artifact field version we set a value in.
     */
    private void saveArtifactValueInner(ArtifactFieldStorageType storageType, String value,
                                        ArtifactFieldVersion fieldVersion) {

        IFieldValue fieldValueObj = storageType.getFieldValueConstructor().get();
        fieldValueObj.setFieldVersion(fieldVersion);
        fieldValueObj.setValueFromString(value);
        fieldValueObj.save(serviceProvider);
    }
}
