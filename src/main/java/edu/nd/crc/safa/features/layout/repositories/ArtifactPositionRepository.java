package edu.nd.crc.safa.features.layout.repositories;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactVersion;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.layout.entities.db.ArtifactPosition;

import org.springframework.data.repository.CrudRepository;

public interface ArtifactPositionRepository extends CrudRepository<ArtifactPosition, UUID> {
    Optional<ArtifactPosition> findByArtifactVersionAndDocument(ArtifactVersion artifactVersion, Document document);
}
