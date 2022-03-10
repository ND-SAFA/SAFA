package edu.nd.crc.safa.server.repositories.documents;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.Document;
import edu.nd.crc.safa.server.entities.db.DocumentArtifact;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface DocumentArtifactRepository extends CrudRepository<DocumentArtifact, UUID> {

    List<DocumentArtifact> findByProjectVersionAndArtifact(ProjectVersion projectVersion, Artifact artifact);

    Optional<DocumentArtifact> findByProjectVersionAndDocumentAndArtifact(ProjectVersion projectVersion,
                                                                          Document document,
                                                                          Artifact artifact);

    List<DocumentArtifact> findByDocument(Document document);

    Optional<DocumentArtifact> findByDocumentDocumentIdAndArtifact(UUID documentId, Artifact artifact);

    Optional<DocumentArtifact> findByDocumentAndArtifactArtifactId(Document document, UUID artifactId);
}
