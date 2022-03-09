package edu.nd.crc.safa.server.repositories.artifacts;

import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.ArtifactType;
import edu.nd.crc.safa.server.entities.db.ArtifactVersion;
import edu.nd.crc.safa.server.entities.db.Document;
import edu.nd.crc.safa.server.entities.db.DocumentArtifact;
import edu.nd.crc.safa.server.entities.db.DocumentType;
import edu.nd.crc.safa.server.entities.db.FTAArtifact;
import edu.nd.crc.safa.server.entities.db.ModificationType;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.entities.db.SafetyCaseArtifact;
import edu.nd.crc.safa.server.repositories.GenericVersionRepository;
import edu.nd.crc.safa.server.repositories.documents.DocumentArtifactRepository;
import edu.nd.crc.safa.server.repositories.documents.DocumentRepository;

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

    @Autowired
    DocumentArtifactRepository documentArtifactRepository;

    @Autowired
    DocumentRepository documentRepository;

    @Autowired
    FTAArtifactRepository ftaArtifactRepository;

    @Autowired
    SafetyCaseArtifactRepository safetyCaseArtifactRepository;

    @Override
    public List<ArtifactVersion> getVersionEntitiesByProject(Project project) {
        return artifactVersionRepository.findByProjectVersionProject(project);
    }

    @Override
    public List<ArtifactVersion> getVersionEntitiesByBaseEntity(Artifact artifact) {
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
    public Artifact findOrCreateBaseEntitiesFromAppEntity(ProjectVersion projectVersion,
                                                          ArtifactAppEntity artifactAppEntity) throws SafaError {
        Project project = projectVersion.getProject();
        String artifactId = artifactAppEntity.getId();
        String typeName = artifactAppEntity.type;
        String artifactName = artifactAppEntity.name;
        DocumentType documentType = artifactAppEntity.getDocumentType();

        ArtifactType artifactType = findOrCreateArtifactType(project, typeName);
        Artifact artifact = createOrUpdateArtifact(project, artifactId, artifactName, artifactType, documentType);
        createOrUpdateDocumentIds(projectVersion, artifact, artifactAppEntity.getDocumentIds());

        switch (artifactAppEntity.getDocumentType()) {
            case FTA:
                String parentTypeName = artifactAppEntity.getParentType();
                this
                    .artifactTypeRepository
                    .findByProjectAndNameIgnoreCase(project, parentTypeName)
                    .ifPresent(parentType -> {
                        FTAArtifact ftaArtifact = new FTAArtifact(artifact,
                            parentType,
                            artifactAppEntity.getLogicType());
                        this.ftaArtifactRepository.save(ftaArtifact);
                    });
                break;
            case SAFETY_CASE:
                SafetyCaseArtifact safetyCaseArtifact = new SafetyCaseArtifact(artifact,
                    artifactAppEntity.getSafetyCaseType());
                this.safetyCaseArtifactRepository.save(safetyCaseArtifact);
                break;
            default:
                break;
        }

        artifactAppEntity.setId(artifactId);
        return artifact;
    }

    @Override
    public void saveOrOverrideVersionEntity(ProjectVersion projectVersion,
                                            ArtifactVersion newArtifactVersion) throws SafaError {
        try {
            //Overriding any version equal to given
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
    public List<Artifact> getBaseEntitiesByProject(Project project) {
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
    public Optional<Artifact> findBaseEntityById(String baseEntityId) {
        return this.artifactRepository.findById(UUID.fromString(baseEntityId));
    }

    @Override
    public ArtifactAppEntity createAppFromVersion(ArtifactVersion versionEntity) {
        return new ArtifactAppEntity(versionEntity);
    }

    private void createOrUpdateDocumentIds(ProjectVersion projectVersion,
                                           Artifact artifact,
                                           List<String> incomingDocumentIds) {
        List<String> persistedDocumentIds = documentArtifactRepository.findByProjectVersionAndArtifact(projectVersion, artifact)
            .stream()
            .map(da -> da.getDocument().getDocumentId().toString())
            .collect(Collectors.toList());

        List<String> newDocumentIds = incomingDocumentIds
            .stream()
            .filter(newDocumentId -> !persistedDocumentIds.contains(newDocumentId))
            .collect(Collectors.toList());

        for (String newDocumentId : newDocumentIds) {
            Optional<Document> documentQuery = this.documentRepository.findById(UUID.fromString(newDocumentId));
            if (documentQuery.isPresent()) {
                Document document = documentQuery.get();
                DocumentArtifact documentArtifact = new DocumentArtifact(projectVersion, document, artifact);
                this.documentArtifactRepository.save(documentArtifact);
            }
        }

        List<String> removedDocumentIds = persistedDocumentIds
            .stream()
            .filter(persistedDocumentId -> !incomingDocumentIds.contains(persistedDocumentId))
            .collect(Collectors.toList());

        for (String removedDocumentId : removedDocumentIds) {
            Optional<DocumentArtifact> documentArtifactQuery =
                documentArtifactRepository.findByDocumentDocumentIdAndArtifact(UUID.fromString(removedDocumentId),
                    artifact);
            documentArtifactQuery.ifPresent(documentArtifactRepository::delete);
        }
    }

    private Artifact createOrUpdateArtifact(Project project,
                                            String artifactId,
                                            String artifactName,
                                            ArtifactType artifactType,
                                            DocumentType documentType) throws SafaError {
        if (artifactId.equals("")) {
            Artifact newArtifact = this.artifactRepository
                .findByProjectAndName(project, artifactName)
                .orElseGet(() -> new Artifact(project, artifactType, artifactName, documentType));
            this.artifactRepository.save(newArtifact);
            return newArtifact;
        } else {
            Optional<Artifact> artifactOptional = this.artifactRepository
                .findById(UUID.fromString(artifactId));
            if (artifactOptional.isEmpty()) {
                throw new SafaError("Could not find artifact with id:" + artifactId);
            }
            Artifact artifact = artifactOptional.get();
            artifact.setType(artifactType);
            artifact.setName(artifactName);
            artifact.setDocumentType(documentType);
            this.artifactRepository.save(artifact);
            return artifact;
        }
    }

    private ArtifactType findOrCreateArtifactType(Project project, String typeName) {
        ArtifactType artifactType = this.artifactTypeRepository
            .findByProjectAndNameIgnoreCase(project, typeName)
            .orElseGet(() -> new ArtifactType(project, typeName));
        this.artifactTypeRepository.save(artifactType);
        return artifactType;
    }
}
