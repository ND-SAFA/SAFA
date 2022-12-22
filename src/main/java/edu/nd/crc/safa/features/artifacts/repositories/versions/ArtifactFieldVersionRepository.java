package edu.nd.crc.safa.features.artifacts.repositories.versions;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.db.schema.CustomAttribute;
import edu.nd.crc.safa.features.artifacts.entities.db.versions.ArtifactFieldVersion;
import edu.nd.crc.safa.features.artifacts.entities.db.versions.ArtifactVersion;

import org.springframework.data.repository.CrudRepository;

public interface ArtifactFieldVersionRepository extends CrudRepository<ArtifactFieldVersion, UUID> {
    Optional<ArtifactFieldVersion> findByArtifactVersionAndSchemaField(ArtifactVersion version, CustomAttribute schemaField);

    List<ArtifactFieldVersion> findByArtifactVersion(ArtifactVersion version);

    List<ArtifactFieldVersion> findBySchemaField(CustomAttribute schemaField);
}
