package edu.nd.crc.safa.features.layout.repositories;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.layout.entities.db.ArtifactPosition;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import org.springframework.data.repository.CrudRepository;

public interface ArtifactPositionRepository extends CrudRepository<ArtifactPosition, UUID> {
    Optional<ArtifactPosition> findByProjectVersionAndArtifactIdAndDocumentDocumentId(
        ProjectVersion projectVersion,
        UUID artifactId,
        UUID documentId);

    List<ArtifactPosition> findByProjectVersionProjectAndDocumentDocumentId(Project project,
                                                                            UUID documentId);

    default List<ArtifactPosition> getByProjectAndDocumentId(Project project, UUID documentId) {
        return findByProjectVersionProjectAndDocumentDocumentId(project, documentId);
    }
}
