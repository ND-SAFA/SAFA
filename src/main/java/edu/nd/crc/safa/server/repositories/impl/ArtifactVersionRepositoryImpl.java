package edu.nd.crc.safa.server.repositories.impl;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.AddedArtifact;
import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.DeltaArtifact;
import edu.nd.crc.safa.server.entities.app.ModifiedArtifact;
import edu.nd.crc.safa.server.entities.app.RemovedArtifact;
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
    extends GenericVersionRepository<Artifact, ArtifactVersion, ArtifactAppEntity, DeltaArtifact> {

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

    public Artifact findOrCreateBaseEntityFromAppEntity(Project project,
                                                        ArtifactAppEntity artifactAppEntity) {
        String artifactId = artifactAppEntity.getId();
        String typeName = artifactAppEntity.getType();
        String artifactName = artifactAppEntity.getName();

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
    public void saveOrOverrideVersionEntity(ProjectVersion projectVersion,
                                            ArtifactVersion newArtifactVersion) throws SafaError {
        try {
            this.artifactVersionRepository
                .findByProjectVersionAndArtifactName(projectVersion, newArtifactVersion.getName())
                .ifPresent((existingVersionEntity) -> {
                    artifactVersionRepository.delete(existingVersionEntity);
                });
            this.artifactVersionRepository.save(newArtifactVersion);
        } catch (Exception e) {
            String error = String.format("An error occurred while saving artifact: %s", newArtifactVersion.getName());
            throw new SafaError(error, e);
        }
    }

    @Override
    public List<Artifact> getBaseEntitiesInProject(Project project) {
        return this.artifactRepository.findByProject(project);
    }

    @Override
    public ArtifactVersion createRemovedVersionEntity(ProjectVersion projectVersion,
                                                      Artifact artifact) {
        return new ArtifactVersion(
            projectVersion,
            ModificationType.REMOVED,
            artifact,
            "", "");
    }

    @Override
    public Optional<Artifact> findBaseEntityByName(Project project, String name) {
        return this.artifactRepository.findByProjectAndName(project, name);
    }

    @Override
    public DeltaArtifact createDeltaEntity(ModificationType modificationType,
                                           String baseEntityName,
                                           ArtifactVersion baseVersionEntity,
                                           ArtifactVersion targetVersionEntity) {
        switch (modificationType) {
            case MODIFIED:
                return new ModifiedArtifact(baseEntityName,
                    baseVersionEntity.getContent(),
                    baseVersionEntity.getSummary(),
                    targetVersionEntity.getContent(),
                    targetVersionEntity.getSummary());
            case ADDED:
                return new AddedArtifact(baseEntityName,
                    targetVersionEntity.getContent(),
                    targetVersionEntity.getSummary());
            case REMOVED:
                return new RemovedArtifact(baseEntityName,
                    baseVersionEntity.getContent(),
                    baseVersionEntity.getSummary());
            default:
                return null;
        }
    }

    @Override
    public List<ArtifactVersion> findVersionEntitiesWithBaseEntity(Artifact baseEntity) {
        return this.artifactVersionRepository.findByArtifact(baseEntity);
    }
}
