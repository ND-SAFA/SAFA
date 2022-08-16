package edu.nd.crc.safa.features.layout.repositories;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.layout.entities.db.ArtifactPosition;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

import org.springframework.data.repository.CrudRepository;

public interface ArtifactPositionRepository extends CrudRepository<ArtifactPosition, UUID> {
    Optional<ArtifactPosition> findByProjectVersionAndArtifactAndDocumentDocumentId(
        ProjectVersion projectVersion,
        Artifact artifact,
        UUID documentId);

    List<ArtifactPosition> findByProjectVersionAndDocument(ProjectVersion projectVersion, Document document);

    List<ArtifactPosition> findByProjectVersionAndDocumentDocumentId(ProjectVersion projectVersion, UUID documentId);
}
