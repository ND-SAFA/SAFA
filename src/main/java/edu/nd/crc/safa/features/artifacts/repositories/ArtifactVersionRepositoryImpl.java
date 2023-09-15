package edu.nd.crc.safa.features.artifacts.repositories;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactVersion;
import edu.nd.crc.safa.features.artifacts.entities.db.FTAArtifact;
import edu.nd.crc.safa.features.artifacts.entities.db.SafetyCaseArtifact;
import edu.nd.crc.safa.features.attributes.services.AttributeValueService;
import edu.nd.crc.safa.features.commits.repositories.GenericVersionRepository;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.documents.entities.db.DocumentArtifact;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.documents.repositories.DocumentArtifactRepository;
import edu.nd.crc.safa.features.documents.repositories.DocumentRepository;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.app.SafaItemNotFoundError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.entities.db.ProjectEntity;
import edu.nd.crc.safa.features.types.entities.db.ArtifactType;
import edu.nd.crc.safa.features.types.entities.db.ArtifactTypeCount;
import edu.nd.crc.safa.features.types.services.ArtifactTypeCountService;
import edu.nd.crc.safa.features.types.services.TypeService;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import com.fasterxml.jackson.databind.JsonNode;
import org.springframework.beans.factory.annotation.Autowired;

/**
 * Implements custom any custom artifact repository logic.
 */
public class ArtifactVersionRepositoryImpl
    extends GenericVersionRepository<Artifact, ArtifactVersion, ArtifactAppEntity> {

    @Autowired
    private ArtifactVersionRepository artifactVersionRepository;

    @Autowired
    private ArtifactRepository artifactRepository;

    @Autowired
    private TypeService artifactTypeService;

    @Autowired
    private DocumentArtifactRepository documentArtifactRepository;

    @Autowired
    private DocumentRepository documentRepository;

    @Autowired
    private FTAArtifactRepository ftaArtifactRepository;

    @Autowired
    private SafetyCaseArtifactRepository safetyCaseArtifactRepository;

    @Autowired
    private AttributeValueService attributeValueService;

    @Autowired
    private ArtifactTypeCountService typeCountService;

    @Override
    public ArtifactVersion save(ArtifactVersion artifactVersion) {
        ArtifactVersion version = this.artifactVersionRepository.save(artifactVersion);

        attributeValueService.saveAllAttributeValues(artifactVersion,
            artifactVersion.getCustomAttributeValues());

        return version;
    }

    @Override
    public ArtifactVersion instantiateVersionEntityWithModification(ProjectVersion projectVersion,
                                                                    ModificationType modificationType,
                                                                    Artifact artifact,
                                                                    ArtifactAppEntity artifactAppEntity) {
        if (modificationType == ModificationType.REMOVED || artifactAppEntity == null) {
            return new ArtifactVersion(projectVersion,
                ModificationType.REMOVED,
                artifact,
                "",
                "");
        }
        ArtifactVersion artifactVersion = new ArtifactVersion(projectVersion,
            modificationType,
            artifact,
            artifactAppEntity.getSummary(),
            artifactAppEntity.getBody());

        for (Map.Entry<String, JsonNode> entry : artifactAppEntity.getAttributes().entrySet()) {
            artifactVersion.addCustomAttributeValue(entry.getKey(), entry.getValue());
        }

        return artifactVersion;
    }

    @Override
    protected ProjectEntity getProjectActivity() {
        return ProjectEntity.ARTIFACTS;
    }

    @Override
    public Artifact createOrUpdateRelatedEntities(ProjectVersion projectVersion,
                                                  ArtifactAppEntity artifactAppEntity,
                                                  SafaUser user) throws SafaError {
        Artifact artifact = createOrUpdateArtifactFromAppEntity(projectVersion.getProject(), artifactAppEntity, user);
        artifactAppEntity.setId(artifactAppEntity.getId());

        createOrUpdateDocumentIds(projectVersion, artifact, artifactAppEntity.getDocumentIds());
        createOrUpdateDocumentNodeInformation(artifactAppEntity, artifact);
        return artifact;
    }

    @Override
    public Optional<ArtifactVersion> findExistingVersionEntity(ArtifactVersion artifactVersion) {
        Optional<ArtifactVersion> version = this.artifactVersionRepository
            .findByProjectVersionAndArtifactName(artifactVersion.getProjectVersion(), artifactVersion.getName());
        version.ifPresent(attributeValueService::attachCustomAttributesToArtifact);
        return version;
    }

    @Override
    public Optional<Artifact> findBaseEntityById(UUID baseEntityId) {
        return this.artifactRepository.findById(baseEntityId);
    }

    @Override
    public List<ArtifactVersion> retrieveVersionEntitiesByProject(Project project) {
        List<ArtifactVersion> versions = artifactVersionRepository.findByProjectVersionProject(project);
        attributeValueService.attachCustomAttributesToArtifacts(versions);
        return versions;
    }

    @Override
    public List<ArtifactVersion> retrieveVersionEntitiesByBaseIds(List<UUID> baseIds) {
        return artifactVersionRepository.findByArtifactArtifactIdIn(baseIds);
    }

    @Override
    public List<ArtifactVersion> retrieveVersionEntitiesByBaseEntity(Artifact artifact) {
        List<ArtifactVersion> versions = artifactVersionRepository.findByArtifact(artifact);
        attributeValueService.attachCustomAttributesToArtifacts(versions);
        return versions;
    }

    @Override
    public List<Artifact> retrieveBaseEntitiesByProject(Project project) {
        return this.artifactRepository.findByProject(project);
    }

    @Override
    public ArtifactAppEntity retrieveAppEntityFromVersionEntity(ArtifactVersion artifactVersion) {
        // Step 1 - Create base entity information

        ArtifactAppEntity artifactAppEntity = new ArtifactAppEntity(
            artifactVersion.getArtifact().getArtifactId(),
            artifactVersion.getTypeName(),
            artifactVersion.getName(),
            artifactVersion.getSummary(),
            artifactVersion.getContent(),
            artifactVersion.getArtifact().getDocumentType(),
            artifactVersion.getCustomAttributeValues());

        // Step 2 - Attach document links
        attachDocumentLinks(artifactVersion, artifactAppEntity);

        // Step 3 - Attach Safety Case or FTA information
        attachDocumentNodeInformation(artifactAppEntity, artifactVersion.getArtifact());
        return artifactAppEntity;
    }

    @Override
    public void updateTimInfo(ProjectVersion projectVersion, ArtifactVersion versionEntity,
                              ArtifactVersion previousVersionEntity, SafaUser user) {
        ModificationType modificationType = versionEntity.getModificationType();
        boolean added = modificationType == ModificationType.ADDED && previousVersionEntity == null;
        boolean removed = modificationType == ModificationType.REMOVED;

        if (added || removed) {
            // TODO this might need to get a table lock somehow if simultaneous updates come in from different sources

            ArtifactType type = versionEntity.getType();
            ArtifactTypeCount typeCount = typeCountService.getByProjectVersionAndType(projectVersion, type)
                .orElseThrow(() -> new SafaItemNotFoundError("Missing type count object for %s", type.getName()));

            if (added) {
                typeCount.setCount(typeCount.getCount() + 1);
            } else {
                typeCount.setCount(typeCount.getCount() - 1);
            }

            typeCountService.save(typeCount);
        }
    }

    /**
     * Private helper methods
     */

    private void attachDocumentLinks(ArtifactVersion artifactVersion,
                                     ArtifactAppEntity artifactAppEntity) {
        //TODO: Skipping versioning system, currently using artifact version which is not usually the user wants.
        Artifact artifact = artifactVersion.getArtifact();
        List<DocumentArtifact> allDocumentArtifactVersions = this.documentArtifactRepository.findByArtifact(artifact);
        List<UUID> documentIds = new ArrayList<>();
        for (DocumentArtifact documentArtifact : allDocumentArtifactVersions) {
            documentIds.add(documentArtifact.getDocument().getDocumentId());
        }

        artifactAppEntity.setDocumentIds(documentIds);
    }

    private void attachDocumentNodeInformation(ArtifactAppEntity artifactAppEntity, Artifact artifact) {
        switch (artifact.getDocumentType()) {
            case SAFETY_CASE:
                Optional<SafetyCaseArtifact> safetyCaseArtifactOptional =
                    this.safetyCaseArtifactRepository.findByArtifact(artifact);
                if (safetyCaseArtifactOptional.isPresent()) {
                    SafetyCaseArtifact safetyCaseArtifact = safetyCaseArtifactOptional.get();
                    artifactAppEntity.setDocumentType(DocumentType.SAFETY_CASE);
                    artifactAppEntity.setSafetyCaseType(safetyCaseArtifact.getSafetyCaseType());
                }
                //TODO: Throw error if not found?
                break;
            case FTA:
                Optional<FTAArtifact> ftaArtifactOptional = this.ftaArtifactRepository.findByArtifact(artifact);
                if (ftaArtifactOptional.isPresent()) {
                    FTAArtifact ftaArtifact = ftaArtifactOptional.get();
                    artifactAppEntity.setDocumentType(DocumentType.FTA);
                    artifactAppEntity.setLogicType(ftaArtifact.getLogicType());
                }
                break;
            default:
                break;
        }
    }

    public void createOrUpdateDocumentNodeInformation(ArtifactAppEntity artifactAppEntity, Artifact artifact) {
        switch (artifactAppEntity.getDocumentType()) {
            case FTA:
                FTAArtifact ftaArtifact;
                Optional<FTAArtifact> ftaArtifactOptional = this.ftaArtifactRepository.findByArtifact(artifact);

                if (ftaArtifactOptional.isPresent()) {
                    ftaArtifact = ftaArtifactOptional.get();
                    ftaArtifact.setLogicType(artifactAppEntity.getLogicType());
                } else {
                    ftaArtifact = new FTAArtifact(artifact, artifactAppEntity.getLogicType());
                }

                this.ftaArtifactRepository.save(ftaArtifact);
                break;
            case SAFETY_CASE:
                SafetyCaseArtifact safetyCaseArtifact;
                Optional<SafetyCaseArtifact> safetyCaseArtifactOptional =
                    this.safetyCaseArtifactRepository.findByArtifact(artifact);
                if (safetyCaseArtifactOptional.isPresent()) {
                    safetyCaseArtifact = safetyCaseArtifactOptional.get();
                    safetyCaseArtifact.setSafetyCaseType(artifactAppEntity.getSafetyCaseType());
                } else {
                    safetyCaseArtifact = new SafetyCaseArtifact(artifact, artifactAppEntity.getSafetyCaseType());
                }
                this.safetyCaseArtifactRepository.save(safetyCaseArtifact);
                break;
            default:
                break;
        }
    }

    private void createOrUpdateDocumentIds(ProjectVersion projectVersion,
                                           Artifact artifact,
                                           List<UUID> incomingDocumentIds) {
        List<UUID> persistedDocumentIds = documentArtifactRepository
            //TODO: Implement document versioning
            .findByProjectVersionProjectAndArtifact(projectVersion.getProject(), artifact)
            .stream()
            .map(da -> da.getDocument().getDocumentId())
            .collect(Collectors.toList());

        List<UUID> newDocumentIds = incomingDocumentIds
            .stream()
            .filter(newDocumentId -> !persistedDocumentIds.contains(newDocumentId))
            .collect(Collectors.toList());

        for (UUID newDocumentId : newDocumentIds) {
            Optional<Document> documentQuery = this.documentRepository.findById(newDocumentId);
            if (documentQuery.isPresent()) {
                Document document = documentQuery.get();
                DocumentArtifact documentArtifact = new DocumentArtifact(projectVersion, document, artifact);
                this.documentArtifactRepository.save(documentArtifact);
            }
        }

        List<UUID> removedDocumentIds = persistedDocumentIds
            .stream()
            .filter(persistedDocumentId -> !incomingDocumentIds.contains(persistedDocumentId))
            .collect(Collectors.toList());

        for (UUID removedDocumentId : removedDocumentIds) {
            Optional<DocumentArtifact> documentArtifactQuery =
                documentArtifactRepository.findByDocumentDocumentIdAndArtifact(removedDocumentId,
                    artifact);
            documentArtifactQuery.ifPresent(documentArtifactRepository::delete);
        }
    }

    private Artifact createOrUpdateArtifactFromAppEntity(Project project, ArtifactAppEntity artifactAppEntity,
                                                         SafaUser user) throws SafaError {
        UUID artifactId = artifactAppEntity.getId();
        String typeName = artifactAppEntity.getType();
        String artifactName = artifactAppEntity.getName();
        ArtifactType artifactType = findOrCreateArtifactType(project, typeName, user);
        DocumentType documentType = artifactAppEntity.getDocumentType();
        if (artifactId == null) {
            Artifact newArtifact = this.artifactRepository
                .findByProjectAndName(project, artifactName)
                .orElseGet(() -> new Artifact(project, artifactType, artifactName, documentType));
            this.artifactRepository.save(newArtifact);
            return newArtifact;
        } else {
            Optional<Artifact> artifactOptional = this.artifactRepository
                .findById(artifactId);
            if (artifactOptional.isEmpty()) {
                throw new SafaError("Could not find artifact with id: %s", artifactId);
            }
            Artifact artifact = artifactOptional.get();
            artifact.setType(artifactType);
            artifact.setName(artifactName);
            artifact.setDocumentType(documentType);
            this.artifactRepository.save(artifact);
            return artifact;
        }
    }

    private ArtifactType findOrCreateArtifactType(Project project, String typeName, SafaUser user) {
        ArtifactType artifactType = this.artifactTypeService.getArtifactType(project, typeName);
        if (artifactType == null) {
            artifactType = this.artifactTypeService.createArtifactType(project, typeName, user);
        }
        return artifactType;
    }
}
