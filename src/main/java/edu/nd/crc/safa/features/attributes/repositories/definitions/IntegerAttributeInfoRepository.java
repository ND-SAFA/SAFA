package edu.nd.crc.safa.features.attributes.repositories.definitions;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.attributes.entities.db.definitions.CustomAttribute;
import edu.nd.crc.safa.features.attributes.entities.db.definitions.IntegerAttributeInfo;

import org.springframework.data.repository.CrudRepository;

public interface IntegerAttributeInfoRepository extends CrudRepository<IntegerAttributeInfo, UUID> {
    Optional<IntegerAttributeInfo> findByAttribute(CustomAttribute attribute);
}
