package edu.nd.crc.safa.features.attributes.repositories.values;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.attributes.entities.db.values.ArtifactAttributeVersion;
import edu.nd.crc.safa.features.attributes.entities.db.values.FloatAttributeValue;

import org.springframework.data.repository.CrudRepository;

public interface FloatAttributeValueRepository extends CrudRepository<FloatAttributeValue, UUID> {
    Optional<FloatAttributeValue> getByAttributeVersion(ArtifactAttributeVersion attributeVersion);
}
