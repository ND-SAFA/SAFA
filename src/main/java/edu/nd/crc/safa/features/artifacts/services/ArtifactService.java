package edu.nd.crc.safa.features.artifacts.services;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactVersion;
import edu.nd.crc.safa.features.artifacts.repositories.IVersionRepository;
import edu.nd.crc.safa.features.common.IAppEntityService;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@AllArgsConstructor
@Service
public class ArtifactService implements IAppEntityService<ArtifactAppEntity> {
    private IVersionRepository<ArtifactVersion, ArtifactAppEntity> artifactVersionRepository;

    /**
     * Returns all artifacts present in the given version.
     *
     * @param projectVersion The project version to retrieve artifacts from.
     * @return The artifacts at current version.
     */
    public List<ArtifactAppEntity> getAppEntities(ProjectVersion projectVersion) {
        return getAppEntities(projectVersion, null);
    }

    /**
     * Returns all artifacts present in the given version.
     *
     * @param projectVersion The project version to retrieve artifacts from.
     * @param user           The user used to retrieve the entities (optional).
     * @return The artifacts at current version.
     */
    @Override
    public List<ArtifactAppEntity> getAppEntities(ProjectVersion projectVersion, SafaUser user) {
        List<ArtifactVersion> artifactVersions = this.artifactVersionRepository
            .retrieveVersionEntitiesByProjectVersion(projectVersion);
        return versionToAppEntity(artifactVersions);
    }

    @Override
    public List<ArtifactAppEntity> getAppEntitiesByIds(ProjectVersion projectVersion, SafaUser user, List<UUID> entityIds) {
        return getAppEntitiesByIds(projectVersion, entityIds);
    }

    /**
     * Returns all versions of all artifacts in the project.
     *
     * @param project The project whose artifacts are retrieved.
     * @return All artifacts across all versions of their lifetime.
     */
    public List<ArtifactAppEntity> getAppEntities(Project project) {
        List<ArtifactVersion> artifactVersions = this.artifactVersionRepository
            .retrieveVersionEntitiesByProject(project);
        return versionToAppEntity(artifactVersions);
    }

    /**
     * Retrieves the artifacts at the version specified.
     *
     * @param projectVersion The project version of the artifacts to retrieve.
     * @param artifactIds    The IDs of the artifacts to retrieve.
     * @return The constructed artifacts at given version.
     */
    public List<ArtifactAppEntity> getAppEntitiesByIds(ProjectVersion projectVersion, List<UUID> artifactIds) {
        List<ArtifactVersion> artifactVersions = new ArrayList<>();
        for (UUID artifactId : artifactIds) {
            Optional<ArtifactVersion> artifactVersionOptional =
                this.artifactVersionRepository.findVersionEntityByProjectVersionAndBaseEntityId(projectVersion,
                    artifactId);
            artifactVersionOptional.ifPresent(artifactVersions::add);
        }
        return versionToAppEntity(artifactVersions);
    }

    private List<ArtifactAppEntity> versionToAppEntity(List<ArtifactVersion> artifactVersions) {
        List<ArtifactAppEntity> artifacts = new ArrayList<>();
        for (ArtifactVersion artifactVersion : artifactVersions) {
            ArtifactAppEntity artifactAppEntity = this.artifactVersionRepository
                .retrieveAppEntityFromVersionEntity(artifactVersion);
            artifacts.add(artifactAppEntity);
        }
        return artifacts;
    }
}
