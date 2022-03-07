package edu.nd.crc.safa.server.repositories.entities.artifacts;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.FTAArtifact;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface FTAArtifactRepository extends CrudRepository<FTAArtifact, UUID> {

    Optional<FTAArtifact> findByArtifact(Artifact artifact);
}
