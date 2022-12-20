package edu.nd.crc.safa.features.artifacts.repositories.versions;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.db.versions.ArtifactFieldVersion;
import edu.nd.crc.safa.features.artifacts.entities.db.versions.IntegerFieldValue;

import org.springframework.data.repository.CrudRepository;

public interface IntegerFieldValueRepository extends CrudRepository<IntegerFieldValue, UUID> {
    Optional<IntegerFieldValue> getByFieldVersion(ArtifactFieldVersion fieldVersion);
}
