package edu.nd.crc.safa.features.attributes.repositories.values;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactVersion;
import edu.nd.crc.safa.features.attributes.entities.db.definitions.CustomAttribute;
import edu.nd.crc.safa.features.attributes.entities.db.values.ArtifactAttributeVersion;

import org.springframework.data.repository.CrudRepository;

public interface ArtifactAttributeVersionRepository extends CrudRepository<ArtifactAttributeVersion, UUID> {
    Optional<ArtifactAttributeVersion> findByArtifactVersionAndAttribute(ArtifactVersion version, CustomAttribute attribute);

    List<ArtifactAttributeVersion> findByArtifactVersion(ArtifactVersion version);

    List<ArtifactAttributeVersion> findByAttribute(CustomAttribute attribute);
}
