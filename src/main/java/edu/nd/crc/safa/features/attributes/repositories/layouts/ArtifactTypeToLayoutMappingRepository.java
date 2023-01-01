package edu.nd.crc.safa.features.attributes.repositories.layouts;

import java.util.UUID;

import edu.nd.crc.safa.features.attributes.entities.db.layouts.ArtifactTypeToLayoutMapping;

import org.springframework.data.repository.CrudRepository;

public interface ArtifactTypeToLayoutMappingRepository extends CrudRepository<ArtifactTypeToLayoutMapping, UUID> {
}
