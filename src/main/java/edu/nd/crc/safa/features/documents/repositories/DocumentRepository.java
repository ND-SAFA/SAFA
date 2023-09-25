package edu.nd.crc.safa.features.documents.repositories;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.projects.entities.db.Project;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface DocumentRepository extends CrudRepository<Document, UUID> {

    List<Document> findByProject(Project project);

    List<Document> findByProjectAndDocumentIdIn(Project project, List<UUID> entityIds);
}
