package edu.nd.crc.safa.database.repositories;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.database.entities.Artifact;
import edu.nd.crc.safa.database.entities.ArtifactType;
import edu.nd.crc.safa.database.entities.Project;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ArtifactRepository extends CrudRepository<Artifact, UUID> {

    Artifact findByArtifactId(String artifactId);

    Artifact findByProjectAndArtifactTypeAndName(Project project, ArtifactType artifactType, String name);

    List<Artifact> findByProjectId(String projectId);
}
