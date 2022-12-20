package edu.nd.crc.safa.features.artifacts.repositories.versions;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.db.versions.ArtifactFieldVersion;
import edu.nd.crc.safa.features.artifacts.entities.db.versions.BooleanFieldValue;

import org.springframework.data.repository.CrudRepository;

public interface BooleanFieldValueRepository extends CrudRepository<BooleanFieldValue, UUID>  {

    Optional<BooleanFieldValue> getByFieldVersion(ArtifactFieldVersion fieldVersion);
}
