package edu.nd.crc.safa.server.repositories.impl;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.ArtifactType;
import edu.nd.crc.safa.server.entities.db.ArtifactVersion;
import edu.nd.crc.safa.server.entities.db.ModificationType;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.ArtifactRepository;
import edu.nd.crc.safa.server.repositories.ArtifactTypeRepository;
import edu.nd.crc.safa.server.repositories.ArtifactVersionRepository;

import org.springframework.beans.factory.annotation.Autowired;

/**
 * Implements custom any custom artifact repository logic.
 */
public class ArtifactVersionRepositoryImpl
    extends GenericVersionRepository<Artifact, ArtifactVersion, ArtifactAppEntity> {

    @Autowired
    ArtifactVersionRepository artifactVersionRepository;

    @Autowired
    ArtifactRepository artifactRepository;

    @Autowired
    ArtifactTypeRepository artifactTypeRepository;

    @Override
    public List<ArtifactVersion> getEntitiesInProject(Project project) {
        return artifactVersionRepository.findByProjectVersionProject(project);
    }

    @Override
    public List<ArtifactVersion> findByEntity(Artifact artifact) {
        return artifactVersionRepository.findByArtifact(artifact);
    }

    @Override
    public ArtifactVersion createEntityVersionWithModification(ProjectVersion projectVersion,
                                                               ModificationType modificationType,
                                                               Artifact artifact,
                                                               ArtifactAppEntity artifactAppEntity) {
        switch (modificationType) {
            case ADDED:
                return new ArtifactVersion(projectVersion,
                    ModificationType.ADDED,
                    artifact,
                    artifactAppEntity.summary,
                    artifactAppEntity.body);
            case MODIFIED:
                return new ArtifactVersion(projectVersion,
                    ModificationType.MODIFIED,
                    artifact,
                    artifactAppEntity.summary,
                    artifactAppEntity.body);
            case REMOVED:
                return new ArtifactVersion(projectVersion,
                    ModificationType.REMOVED,
                    artifact,
                    "",
                    "");
            default:
                throw new RuntimeException("Missing case in delta service.");
        }
    }

    @Override
    public Optional<ArtifactVersion> findEntityVersionInProjectVersion(ProjectVersion projectVersion,
                                                                       Artifact artifact) {
        return artifactVersionRepository.findByProjectVersionAndArtifact(projectVersion, artifact);
    }

    public Artifact findOrCreateBaseEntityFromAppEntity(ProjectVersion projectVersion,
                                                        ArtifactAppEntity artifactAppEntity) {
        String artifactId = artifactAppEntity.getId();
        String typeName = artifactAppEntity.getType();
        String artifactName = artifactAppEntity.getName();

        Project project = projectVersion.getProject();
        ArtifactType artifactType = findOrCreateArtifactType(project, typeName);
        Artifact artifact = createOrUpdateArtifact(project, artifactId, artifactName, artifactType);

        artifactAppEntity.setId(artifactId);
        return artifact;
    }

    private Artifact createOrUpdateArtifact(Project project,
                                            String artifactId,
                                            String artifactName,
                                            ArtifactType artifactType) {
        if (artifactId.equals("")) {
            Artifact newArtifact = new Artifact(project, artifactType, artifactName);
            this.artifactRepository.save(newArtifact);
            return newArtifact;
        }
        Artifact artifact = this.artifactRepository
            .findById(UUID.fromString(artifactId))
            .orElseGet(() -> new Artifact(project, artifactType, artifactName));
        artifact.setType(artifactType);
        artifact.setName(artifactName);
        this.artifactRepository.save(artifact);
        return artifact;
    }

    private ArtifactType findOrCreateArtifactType(Project project, String typeName) {
        ArtifactType artifactType = this.artifactTypeRepository
            .findByProjectAndNameIgnoreCase(project, typeName)
            .orElseGet(() -> new ArtifactType(project, typeName));
        this.artifactTypeRepository.save(artifactType);
        return artifactType;
    }

    @Override
    public void saveVersionEntity(ArtifactVersion artifactVersion) throws SafaError {
        try {
            this.artifactVersionRepository.save(artifactVersion);
        } catch (Exception e) {
            String error = String.format("An error occurred while saving artifact: %s", artifactVersion.getName());
            throw new SafaError(error, e);
        }
    }

    @Override
    public List<Artifact> getProjectBaseEntities(Project project) {
        return this.artifactRepository.findByProject(project);
    }
}
