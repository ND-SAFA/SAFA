package edu.nd.crc.safa.features.artifacts.repositories;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactVersion;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ArtifactVersionRepository extends CrudRepository<ArtifactVersion, UUID>,
    IVersionRepository<ArtifactVersion, ArtifactAppEntity> {

    List<ArtifactVersion> findByArtifact(Artifact artifact);

    List<ArtifactVersion> findByProjectVersion(ProjectVersion projectVersion);

    int countByProjectVersion(ProjectVersion projectVersion);

    Optional<ArtifactVersion> findByProjectVersionAndArtifact(ProjectVersion projectVersion, Artifact artifact);

    Optional<ArtifactVersion> findByProjectVersionAndArtifactName(ProjectVersion projectVersion, String name);

    List<ArtifactVersion> findByArtifactArtifactIdIn(List<UUID> baseEntityIds);

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
