package edu.nd.crc.safa.server.db.repositories;

import java.util.UUID;

import edu.nd.crc.safa.server.db.entities.sql.ArtifactFile;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TIMFileRepository extends CrudRepository<ArtifactFile, UUID> {

}
