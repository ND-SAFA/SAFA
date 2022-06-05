package edu.nd.crc.safa.server.repositories.documents;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.server.entities.db.CurrentDocument;
import edu.nd.crc.safa.server.entities.db.SafaUser;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface CurrentDocumentRepository extends CrudRepository<CurrentDocument, UUID> {

    Optional<CurrentDocument> findByUser(SafaUser user);
}
