package edu.nd.crc.safa.features.artifacts.repositories.schema;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.db.schema.ArtifactSchemaField;
import edu.nd.crc.safa.features.types.ArtifactType;

import org.springframework.data.repository.CrudRepository;

public interface ArtifactSchemaFieldRepository extends CrudRepository<ArtifactSchemaField, UUID>  {

    Optional<ArtifactSchemaField> findByArtifactTypeAndKeyname(ArtifactType type, String keyname);

    List<ArtifactSchemaField> findByArtifactType(ArtifactType type);
}
