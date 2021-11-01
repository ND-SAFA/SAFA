package edu.nd.crc.safa.server.repositories;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.ArtifactBody;
import edu.nd.crc.safa.server.entities.db.ArtifactType;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ArtifactBodyRepository extends CrudRepository<ArtifactBody, UUID> {

    List<ArtifactBody> findByArtifact(Artifact artifact);

    List<ArtifactBody> findByProjectVersionAndArtifactType(ProjectVersion projectVersion,
                                                           ArtifactType artifactType);

    List<ArtifactBody> findByProjectVersion(ProjectVersion projectVersion);

    Optional<ArtifactBody> findByProjectVersionAndArtifact(ProjectVersion projectVersion, Artifact artifact);

    default List<ArtifactBody> getBodiesWithName(Project project, String name) {
        return findByProjectVersionProjectAndArtifactName(project, name);
    }

    default Optional<ArtifactBody> findLastArtifactBody(Project project, Artifact artifact) {
        return this.findTopByProjectVersionProjectAndArtifactOrderByProjectVersionMajorVersionDescProjectVersionMinorVersionDescProjectVersionRevisionDesc(
            project,
            artifact);
    }

    default List<ArtifactBody> findByProject(Project project) {
        return findByProjectVersionProject(project);
    }

    List<ArtifactBody> findByProjectVersionProjectAndArtifactName(Project project, String name);

    Optional<ArtifactBody> findTopByProjectVersionProjectAndArtifactOrderByProjectVersionMajorVersionDescProjectVersionMinorVersionDescProjectVersionRevisionDesc(
        Project project,
        Artifact artifact);

    List<ArtifactBody> findByProjectVersionProject(Project project);
}
