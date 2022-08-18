package edu.nd.crc.safa.features.artifacts.repositories;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.artifacts.entities.db.SafetyCaseArtifact;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface SafetyCaseArtifactRepository extends
    CrudRepository<SafetyCaseArtifact, UUID> {

    Optional<SafetyCaseArtifact> findByArtifact(Artifact artifact);
}
