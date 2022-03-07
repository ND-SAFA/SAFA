package edu.nd.crc.safa.server.repositories.artifacts;

import java.util.UUID;

import edu.nd.crc.safa.server.entities.db.FTAArtifact;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface FTAArtifactRepository extends CrudRepository<FTAArtifact, UUID> {
}
