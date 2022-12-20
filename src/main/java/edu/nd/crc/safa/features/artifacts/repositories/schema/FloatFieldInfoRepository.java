package edu.nd.crc.safa.features.artifacts.repositories.schema;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.db.schema.ArtifactSchemaField;
import edu.nd.crc.safa.features.artifacts.entities.db.schema.FloatFieldInfo;

import org.springframework.data.repository.CrudRepository;

public interface FloatFieldInfoRepository extends CrudRepository<FloatFieldInfo, UUID> {
    Optional<FloatFieldInfo> findBySchemaField(ArtifactSchemaField schemaField);
}
