package edu.nd.crc.safa.features.artifacts.repositories.schema;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.db.schema.CustomAttribute;
import edu.nd.crc.safa.features.artifacts.entities.db.schema.IntegerFieldInfo;

import org.springframework.data.repository.CrudRepository;

public interface IntegerFieldInfoRepository extends CrudRepository<IntegerFieldInfo, UUID> {
    Optional<IntegerFieldInfo> findBySchemaField(CustomAttribute schemaField);
}
