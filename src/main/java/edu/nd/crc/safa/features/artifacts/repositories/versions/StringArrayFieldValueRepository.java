package edu.nd.crc.safa.features.artifacts.repositories.versions;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.db.versions.ArtifactFieldVersion;
import edu.nd.crc.safa.features.artifacts.entities.db.versions.StringArrayFieldValue;

import org.springframework.data.repository.CrudRepository;

public interface StringArrayFieldValueRepository extends CrudRepository<StringArrayFieldValue, UUID> {
    List<StringArrayFieldValue> getByFieldVersion(ArtifactFieldVersion fieldVersion);
}
