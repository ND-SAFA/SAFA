package edu.nd.crc.safa.features.artifacts.repositories.versions;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.db.versions.ArtifactFieldVersion;
import edu.nd.crc.safa.features.artifacts.entities.db.versions.FloatFieldValue;

import org.springframework.data.repository.CrudRepository;

public interface FloatFieldValueRepository extends CrudRepository<FloatFieldValue, UUID> {
    Optional<FloatFieldValue> getByFieldVersion(ArtifactFieldVersion fieldVersion);
}
