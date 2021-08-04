package edu.nd.crc.safa.database.repositories;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.entities.Artifact;
import edu.nd.crc.safa.entities.ArtifactType;
import edu.nd.crc.safa.entities.Project;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ArtifactRepository extends CrudRepository<Artifact, UUID> {

    Artifact findByProjectAndTypeAndName(Project project, ArtifactType artifactType, String name);

    List<Artifact> findByProject(Project project);

    void deleteAllByProject(Project project);
}
