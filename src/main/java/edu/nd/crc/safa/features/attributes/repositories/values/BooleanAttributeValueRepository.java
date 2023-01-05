package edu.nd.crc.safa.features.attributes.repositories.values;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.attributes.entities.db.values.ArtifactAttributeVersion;
import edu.nd.crc.safa.features.attributes.entities.db.values.BooleanAttributeValue;

import org.springframework.data.repository.CrudRepository;

public interface BooleanAttributeValueRepository extends CrudRepository<BooleanAttributeValue, UUID>  {

    Optional<BooleanAttributeValue> getByAttributeVersion(ArtifactAttributeVersion attributeVersion);
}
