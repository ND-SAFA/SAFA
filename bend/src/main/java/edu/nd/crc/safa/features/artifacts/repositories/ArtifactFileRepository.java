package edu.nd.crc.safa.features.artifacts.repositories;

import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactFile;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ArtifactFileRepository extends CrudRepository<ArtifactFile, UUID> {
}
