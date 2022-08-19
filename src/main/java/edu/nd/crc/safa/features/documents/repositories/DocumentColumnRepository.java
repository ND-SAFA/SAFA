package edu.nd.crc.safa.features.documents.repositories;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.documents.entities.db.DocumentColumn;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface DocumentColumnRepository extends CrudRepository<DocumentColumn, UUID> {

    List<DocumentColumn> findByDocumentOrderByTableColumnIndexAsc(Document document);

    List<DocumentColumn> findByDocumentDocumentIdOrderByTableColumnIndexAsc(UUID documentId);

    List<DocumentColumn> findByDocument(Document document);
}
