package edu.nd.crc.safa.repositories;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.entities.database.Artifact;
import edu.nd.crc.safa.entities.database.ArtifactType;
import edu.nd.crc.safa.entities.database.Project;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ArtifactRepository extends CrudRepository<Artifact, UUID> {

    Optional<Artifact> findByProjectAndName(Project project, String name);

    Optional<Artifact> findByProjectAndTypeAndNameIgnoreCase(Project project, ArtifactType artifactType, String name);

    List<Artifact> findByProject(Project project);

    List<Artifact> findByProjectAndType(Project project, ArtifactType artifactType);

    void deleteAllByProject(Project project);

    Artifact findByArtifactId(UUID artifactId);
}
