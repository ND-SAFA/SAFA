package edu.nd.crc.safa.features.artifacts.repositories.versions;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.db.versions.ArtifactFieldVersion;
import edu.nd.crc.safa.features.artifacts.entities.db.versions.StringFieldValue;

import org.springframework.data.repository.CrudRepository;

public interface StringFieldValueRepository extends CrudRepository<StringFieldValue, UUID> {
    Optional<StringFieldValue> getByFieldVersion(ArtifactFieldVersion fieldVersion);
}
