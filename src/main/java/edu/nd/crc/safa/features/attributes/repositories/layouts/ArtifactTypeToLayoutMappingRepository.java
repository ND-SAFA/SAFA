package edu.nd.crc.safa.features.attributes.repositories.layouts;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.attributes.entities.db.layouts.ArtifactTypeToLayoutMapping;
import edu.nd.crc.safa.features.attributes.entities.db.layouts.AttributeLayout;
import edu.nd.crc.safa.features.types.ArtifactType;

import org.springframework.data.repository.CrudRepository;

public interface ArtifactTypeToLayoutMappingRepository extends CrudRepository<ArtifactTypeToLayoutMapping, UUID> {
    List<ArtifactTypeToLayoutMapping> findByLayout(AttributeLayout layout);

    Optional<ArtifactTypeToLayoutMapping> findByArtifactTypeAndLayout(ArtifactType artifactType, AttributeLayout layout);

    void deleteByLayout(AttributeLayout layout);
}
