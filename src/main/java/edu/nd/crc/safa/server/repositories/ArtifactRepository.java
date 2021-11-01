package edu.nd.crc.safa.server.repositories;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.ArtifactType;
import edu.nd.crc.safa.server.entities.db.Project;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ArtifactRepository extends CrudRepository<Artifact, UUID> {

    Optional<Artifact> findByProjectAndName(Project project, String name);

    List<Artifact> findByProject(Project project);

    List<Artifact> findByProjectAndType(Project project, ArtifactType artifactType);

    default List<Artifact> getProjectArtifacts(Project project) {
        return findByProject(project);
    }
}
