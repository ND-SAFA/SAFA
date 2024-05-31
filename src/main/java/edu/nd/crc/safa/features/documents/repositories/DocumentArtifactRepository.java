package edu.nd.crc.safa.features.documents.repositories;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.documents.entities.db.DocumentArtifact;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface DocumentArtifactRepository extends CrudRepository<DocumentArtifact, UUID> {

    Optional<DocumentArtifact> findByProjectVersionAndDocumentAndArtifact(ProjectVersion projectVersion,
                                                                          Document document,
                                                                          Artifact artifact);

    List<DocumentArtifact> findByDocument(Document document);

    Optional<DocumentArtifact> findByDocumentDocumentIdAndArtifact(UUID documentId, Artifact artifact);

    Optional<DocumentArtifact> findByDocumentAndArtifactArtifactId(Document document, UUID artifactId);

    List<DocumentArtifact> findByProjectVersionProjectAndArtifact(Project project, Artifact artifact);

    List<DocumentArtifact> findByArtifact(Artifact artifact);

    List<DocumentArtifact> findByArtifactIn(List<Artifact> artifacts);
}
