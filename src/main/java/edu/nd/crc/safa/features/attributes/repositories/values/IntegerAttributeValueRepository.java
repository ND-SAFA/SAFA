package edu.nd.crc.safa.features.attributes.repositories.values;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.attributes.entities.db.values.ArtifactAttributeVersion;
import edu.nd.crc.safa.features.attributes.entities.db.values.IntegerAttributeValue;

import org.springframework.data.repository.CrudRepository;

public interface IntegerAttributeValueRepository extends CrudRepository<IntegerAttributeValue, UUID> {
    Optional<IntegerAttributeValue> getByAttributeVersion(ArtifactAttributeVersion attributeVersion);
}
