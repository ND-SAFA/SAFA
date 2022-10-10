package edu.nd.crc.safa.features.artifacts.repositories;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.projects.entities.app.IProjectEntityRetriever;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.types.ArtifactType;

import org.checkerframework.checker.units.qual.A;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ArtifactRepository extends CrudRepository<Artifact, UUID>, IProjectEntityRetriever<Artifact> {

    Optional<Artifact> findByProjectAndName(Project project, String name);

    List<Artifact> findByProject(Project project);

    List<Artifact> findByProjectAndType(Project project, ArtifactType artifactType);

    default List<Artifact> getProjectArtifacts(Project project) {
        return findByProject(project);
    }
}
