package edu.nd.crc.safa.features.attributes.services;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import javax.transaction.Transactional;

import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactVersion;
import edu.nd.crc.safa.features.attributes.entities.db.definitions.CustomAttribute;
import edu.nd.crc.safa.features.attributes.entities.db.values.ArtifactAttributeVersion;
import edu.nd.crc.safa.features.attributes.repositories.values.ArtifactAttributeVersionRepository;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.node.TextNode;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

/**
 * Contains util functions for interacting with artifact fields.
 */
@Service
public class AttributeValueService {

    private final AttributeSystemServiceProvider serviceProvider;

    private final Logger logger = LoggerFactory.getLogger(AttributeValueService.class);
    private final ArtifactAttributeVersionRepository artifactAttributeVersionRepository;

    public AttributeValueService(AttributeSystemServiceProvider serviceProvider,
                                 ArtifactAttributeVersionRepository artifactAttributeVersionRepository) {
        this.serviceProvider = serviceProvider;
        this.artifactAttributeVersionRepository = artifactAttributeVersionRepository;
    }

    /**
     * Gets a map with all the custom attributes that are set for this artifact. The map
     * goes from keyname to json nodes containing the values.
     *
     * @param artifactVersion The artifact version we're looking at.
     * @return A map from attribute keynames to values.
     */
    public Map<String, JsonNode> getCustomAttributeValuesForArtifact(ArtifactVersion artifactVersion) {

        List<ArtifactAttributeVersion> attributeVersions =
            serviceProvider.getArtifactAttributeVersionRepository().findByArtifactVersion(artifactVersion);

        Map<String, JsonNode> out = new HashMap<>();

        for (ArtifactAttributeVersion attributeVersion : attributeVersions) {
            // TODO handle types correctly
            JsonNode jsonValue = TextNode.valueOf(attributeVersion.getValue());

            out.put(attributeVersion.getAttribute().getKeyname(), jsonValue);
        }

        return out;
    }

    /**
     * Saves the given json node as the value of the given attribute within the given version
     * of the given artifact.
     *
     * @param attribute The schema of the attribute we are saving a value to.
     * @param artifactVersion The version of the artifact we are setting a value within.
     * @param value The value to set.
     */
    @Transactional
    public void saveAttributeValue(CustomAttribute attribute, ArtifactVersion artifactVersion, JsonNode value) {
        ArtifactAttributeVersion attributeVersion = getAttributeVersion(attribute, artifactVersion);
        attributeVersion.setValue(value.asText());
        artifactAttributeVersionRepository.save(attributeVersion);
    }

    /**
     * Saves the given json nodes as the values of the given attributes within the given version
     * of the given artifact.
     *
     * @param artifactVersion The version of the artifact we are setting a value within.
     * @param attributeValues The values to set.
     */
    @Transactional
    public void saveAllAttributeValues(ArtifactVersion artifactVersion, Map<String, JsonNode> attributeValues) {

        for (Map.Entry<String, JsonNode> entry : attributeValues.entrySet()) {
            String key = entry.getKey();
            JsonNode value = entry.getValue();

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
     * Gets the current attribute version matching the given attribute and artifact version, if it exists. Else
     * returns a newly constructed one.
     *
     * @param attribute The attribute object we want to access.
     * @param artifactVersion The artifact version we want to access an attribute for.
     * @return The attribute version if it existed previously, or a new one.
     */
    private ArtifactAttributeVersion getAttributeVersion(CustomAttribute attribute, ArtifactVersion artifactVersion) {

        ArtifactAttributeVersionRepository repo = serviceProvider.getArtifactAttributeVersionRepository();

        Optional<ArtifactAttributeVersion> foundAttributeVersion =
            repo.findByArtifactVersionAndAttribute(artifactVersion, attribute);

        return foundAttributeVersion.orElseGet(() -> {
            ArtifactAttributeVersion attributeVersion = new ArtifactAttributeVersion();
            attributeVersion.setArtifactVersion(artifactVersion);
            attributeVersion.setAttribute(attribute);
            repo.save(attributeVersion);
            return attributeVersion;
        });
    }
}
