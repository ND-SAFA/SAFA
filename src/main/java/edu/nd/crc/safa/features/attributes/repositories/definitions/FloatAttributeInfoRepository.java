package edu.nd.crc.safa.features.attributes.repositories.definitions;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.attributes.entities.db.definitions.CustomAttribute;
import edu.nd.crc.safa.features.attributes.entities.db.definitions.FloatAttributeInfo;

import org.springframework.data.repository.CrudRepository;

public interface FloatAttributeInfoRepository extends CrudRepository<FloatAttributeInfo, UUID> {
    Optional<FloatAttributeInfo> findByAttribute(CustomAttribute attribute);
}
