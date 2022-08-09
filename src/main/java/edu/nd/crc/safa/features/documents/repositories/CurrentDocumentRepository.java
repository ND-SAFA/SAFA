package edu.nd.crc.safa.features.documents.repositories;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.documents.entities.db.CurrentDocument;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface CurrentDocumentRepository extends CrudRepository<CurrentDocument, UUID> {

    Optional<CurrentDocument> findByUser(SafaUser user);
}
