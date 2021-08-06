package edu.nd.crc.safa.repositories;

import java.util.UUID;

import edu.nd.crc.safa.entities.ArtifactFile;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ArtifactFileRepository extends CrudRepository<ArtifactFile, UUID> {
}
