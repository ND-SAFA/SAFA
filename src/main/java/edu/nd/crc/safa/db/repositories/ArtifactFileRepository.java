package edu.nd.crc.safa.db.repositories;

import java.util.UUID;

import edu.nd.crc.safa.db.entities.sql.ArtifactFile;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ArtifactFileRepository extends CrudRepository<ArtifactFile, UUID> {
}
