package edu.nd.crc.safa.features.attributes.repositories.values;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.attributes.entities.db.values.ArtifactAttributeVersion;
import edu.nd.crc.safa.features.attributes.entities.db.values.StringAttributeValue;

import org.springframework.data.repository.CrudRepository;

public interface StringAttributeValueRepository extends CrudRepository<StringAttributeValue, UUID> {
    Optional<StringAttributeValue> getByAttributeVersion(ArtifactAttributeVersion attributeVersion);
}
