package edu.nd.crc.safa.features.artifacts.repositories;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.types.entities.db.ArtifactType;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ArtifactRepository extends CrudRepository<Artifact, UUID> {

    Optional<Artifact> findByProjectIdAndName(UUID projectId, String name);

    List<Artifact> findByProjectId(UUID projectId);

    List<Artifact> findByProjectIdAndType(UUID projectId, ArtifactType artifactType);

    default List<Artifact> getProjectArtifacts(UUID projectId) {
        return findByProjectId(projectId);
    }
}
