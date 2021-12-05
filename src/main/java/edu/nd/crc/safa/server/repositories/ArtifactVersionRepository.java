package edu.nd.crc.safa.server.repositories;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.DeltaArtifact;
import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.ArtifactType;
import edu.nd.crc.safa.server.entities.db.ArtifactVersion;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.impl.IVersionRepository;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ArtifactVersionRepository extends CrudRepository<ArtifactVersion, UUID>,
    IVersionRepository<Artifact, ArtifactVersion, ArtifactAppEntity, DeltaArtifact> {

    List<ArtifactVersion> findByArtifact(Artifact artifact);

    List<ArtifactVersion> findByProjectVersionAndArtifactType(ProjectVersion projectVersion,
                                                              ArtifactType artifactType);

    List<ArtifactVersion> findByProjectVersion(ProjectVersion projectVersion);

    Optional<ArtifactVersion> findByProjectVersionAndArtifact(ProjectVersion projectVersion, Artifact artifact);

    Optional<ArtifactVersion> findByProjectVersionAndArtifactName(ProjectVersion projectVersion, String name);

    default List<ArtifactVersion> getBodiesWithName(Project project, String name) {
        return findByProjectVersionProjectAndArtifactName(project, name);
    }

    default Optional<ArtifactVersion> findLastArtifactBody(Project project, Artifact artifact) {
        return this.findTopByProjectVersionProjectAndArtifactOrderByProjectVersionMajorVersionDescProjectVersionMinorVersionDescProjectVersionRevisionDesc(
            project,
            artifact);
    }

    List<ArtifactVersion> findByProjectVersionProjectAndArtifactName(Project project, String name);

    Optional<ArtifactVersion> findTopByProjectVersionProjectAndArtifactOrderByProjectVersionMajorVersionDescProjectVersionMinorVersionDescProjectVersionRevisionDesc(
        Project project,
        Artifact artifact);

    List<ArtifactVersion> findByProjectVersionProject(Project project);
}
