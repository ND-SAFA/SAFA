package edu.nd.crc.safa.db.repositories.sql;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.db.entities.sql.Artifact;
import edu.nd.crc.safa.db.entities.sql.ArtifactBody;
import edu.nd.crc.safa.db.entities.sql.ArtifactType;
import edu.nd.crc.safa.db.entities.sql.Project;
import edu.nd.crc.safa.db.entities.sql.ProjectVersion;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ArtifactBodyRepository extends CrudRepository<ArtifactBody, UUID> {

    List<ArtifactBody> findByArtifact(Artifact artifact);

    List<ArtifactBody> findByProjectVersionAndArtifactType(ProjectVersion projectVersion,
                                                           ArtifactType artifactType);

    List<ArtifactBody> findByProjectVersion(ProjectVersion projectVersion);

    default List<ArtifactBody> getBodiesWithName(Project project, String name) {
        return findByProjectVersionProjectAndArtifactName(project, name);
    }

    List<ArtifactBody> findByProjectVersionProjectAndArtifactName(Project project, String name);

    default Optional<ArtifactBody> findLastArtifactBody(Project project, Artifact artifact) {
        return this.findTopByProjectVersionProjectAndArtifactOrderByProjectVersionDesc(project, artifact);
    }

    Optional<ArtifactBody> findTopByProjectVersionProjectAndArtifactOrderByProjectVersionDesc(Project project,
                                                                                              Artifact artifact);
}
