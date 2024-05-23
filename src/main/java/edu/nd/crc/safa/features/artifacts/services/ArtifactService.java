package edu.nd.crc.safa.features.artifacts.services;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactLookupTable;
import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactVersion;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactRepository;
import edu.nd.crc.safa.features.artifacts.repositories.IVersionRepository;
import edu.nd.crc.safa.features.common.IAppEntityService;
import edu.nd.crc.safa.features.documents.entities.db.DocumentArtifact;
import edu.nd.crc.safa.features.documents.repositories.DocumentArtifactRepository;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.VersionCalculator;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@AllArgsConstructor
@Service
public class ArtifactService implements IAppEntityService<ArtifactAppEntity> {
    private final ArtifactRepository artifactRepository;
    private IVersionRepository<ArtifactVersion, ArtifactAppEntity> artifactVersionRepository;
    private final DocumentArtifactRepository documentArtifactRepository;

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
        attactDocumentsToVersions(artifactVersions);
        return versionToAppEntity(artifactVersions);
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

    private void attactDocumentsToVersions(List<ArtifactVersion> artifactVersions) {
        List<Artifact> artifacts = artifactVersions.stream().map(ArtifactVersion::getArtifact).toList();

        Map<UUID, ArtifactVersion> artifactIdMap = new HashMap<>();
        for (ArtifactVersion artifactVersion : artifactVersions) {
            artifactIdMap.put(artifactVersion.getArtifact().getArtifactId(), artifactVersion);
            artifactVersion.setDocumentIds(new ArrayList<>());
        }

        List<DocumentArtifact> documentArtifacts = documentArtifactRepository.findByArtifactIn(artifacts);
        documentArtifacts.forEach(da -> {
            ArtifactVersion version = artifactIdMap.get(da.getArtifact().getArtifactId());
            version.getDocumentIds().add(da.getDocument().getDocumentId());
        });
    }

    @Override
    public List<ArtifactAppEntity> getAppEntitiesByIds(ProjectVersion projectVersion,
                                                       SafaUser user, List<UUID> appEntityIds) {
        return getAppEntitiesByIds(projectVersion, appEntityIds);
    }

    /**
     * Retrieves the artifacts at the version specified.
     *
     * @param projectVersion The project version of the artifacts to retrieve.
     * @param artifactIds    The IDs of the artifacts to retrieve.
     * @return The constructed artifacts at given version.
     */
    public List<ArtifactAppEntity> getAppEntitiesByIds(ProjectVersion projectVersion, List<UUID> artifactIds) {
        List<ArtifactVersion> allArtifactVersions =
            this.artifactVersionRepository.retrieveVersionEntitiesByBaseIds(artifactIds);
        List<ArtifactVersion> artifactAtVersion = VersionCalculator.getEntitiesAtVersion(projectVersion,
            allArtifactVersions);
        return versionToAppEntity(artifactAtVersion);
    }

    /**
     * Converts list of artifact versions to app entities.
     *
     * @param artifactVersions Artifact versions entities to convert.
     * @return List of artifact app entities.
     */
    public List<ArtifactAppEntity> versionToAppEntity(List<ArtifactVersion> artifactVersions) {
        List<ArtifactAppEntity> artifacts = new ArrayList<>();
        for (ArtifactVersion artifactVersion : artifactVersions) {
            ArtifactAppEntity artifactAppEntity = this.artifactVersionRepository
                .retrieveAppEntityFromVersionEntity(artifactVersion);
            artifacts.add(artifactAppEntity);
        }
        return artifacts;
    }

    /**
     * Retrieves artifact with given ID.
     *
     * @param artifactId ID of artifact.
     * @return Artifact.
     */
    public Artifact findById(UUID artifactId) {
        Optional<Artifact> artifactOptional = artifactRepository.findById(artifactId);
        if (artifactOptional.isEmpty()) {
            throw new SafaError("Could not find artifact with given ID.");
        }
        return artifactOptional.get();
    }

    /**
     * Retrieves generation artifacts for project version.
     *
     * @param projectVersion Version of artifacts to retrieve.
     * @return List of artifacts for GEN.
     */
    public ArtifactLookupTable getArtifactLookupTable(ProjectVersion projectVersion) {
        List<ArtifactVersion> artifactVersions = this.artifactVersionRepository
            .retrieveVersionEntitiesByProjectVersion(projectVersion);
        return new ArtifactLookupTable(artifactVersions);
    }
}
