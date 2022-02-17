package edu.nd.crc.safa.server.repositories;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.server.entities.db.Document;
import edu.nd.crc.safa.server.entities.db.Project;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface DocumentRepository extends CrudRepository<Document, UUID> {

    List<Document> findByProject(Project project);
}
