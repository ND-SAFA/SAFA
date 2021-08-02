package edu.nd.crc.safa.database.repositories;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.database.entities.Artifact;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ArtifactRepository extends CrudRepository<Artifact, UUID> {

    Artifact findById(String artifactId);

    List<Artifact> findByProjectId(String projectId);
}
