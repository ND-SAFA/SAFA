package edu.nd.crc.safa.features.artifacts.repositories;

import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactType;
import edu.nd.crc.safa.features.artifacts.entities.db.ArtifactVersion;
import edu.nd.crc.safa.features.artifacts.entities.db.FTAArtifact;
import edu.nd.crc.safa.features.artifacts.entities.db.SafetyCaseArtifact;
import edu.nd.crc.safa.features.commits.repositories.GenericVersionRepository;
import edu.nd.crc.safa.features.delta.entities.db.ModificationType;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.documents.entities.db.DocumentArtifact;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.documents.repositories.DocumentArtifactRepository;
import edu.nd.crc.safa.features.documents.repositories.DocumentRepository;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.entities.db.ProjectEntity;
import edu.nd.crc.safa.features.traces.repositories.TraceLinkVersionRepository;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;
import edu.nd.crc.safa.utilities.JsonFileUtilities;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
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

    @Autowired
    TraceLinkVersionRepository traceLinkVersionRepository;

    @Override
    public ArtifactVersion save(ArtifactVersion artifactVersion) {
        return this.artifactVersionRepository.save(artifactVersion);
    }

    @Override
    public ArtifactVersion instantiateVersionEntityWithModification(ProjectVersion projectVersion,
                                                                    ModificationType modificationType,
                                                                    Artifact artifact,
                                                                    ArtifactAppEntity artifactAppEntity)
        throws JsonProcessingException {
        if (modificationType == ModificationType.REMOVED || artifactAppEntity == null) {
            return new ArtifactVersion(projectVersion,
                ModificationType.REMOVED,
                artifact,
                "",
                "",
                "");
        }
        return new ArtifactVersion(projectVersion,
            modificationType,
            artifact,
            artifactAppEntity.summary,
            artifactAppEntity.body,
            JsonFileUtilities.toJson(artifactAppEntity.getCustomFields()).toString());
    }

    @Override
    protected ProjectEntity getProjectActivity() {
        return ProjectEntity.ARTIFACTS;
    }

    @Override
    public Artifact createOrUpdateRelatedEntities(ProjectVersion projectVersion,
                                                  ArtifactAppEntity artifactAppEntity) throws SafaError {
        Artifact artifact = createOrUpdateArtifactFromAppEntity(projectVersion.getProject(), artifactAppEntity);
        artifactAppEntity.setBaseEntityId(artifactAppEntity.getBaseEntityId());

        createOrUpdateDocumentIds(projectVersion, artifact, artifactAppEntity.getDocumentIds());
        createOrUpdateDocumentNodeInformation(artifactAppEntity, artifact);
        return artifact;
    }

    @Override
    public Optional<ArtifactVersion> findExistingVersionEntity(ArtifactVersion artifactVersion) {
        return this.artifactVersionRepository
            .findByProjectVersionAndArtifactName(artifactVersion.getProjectVersion(), artifactVersion.getName());
    }

    @Override
    public Optional<Artifact> findBaseEntityById(String baseEntityId) {
        return this.artifactRepository.findById(UUID.fromString(baseEntityId));
    }

    @Override
    public List<ArtifactVersion> retrieveVersionEntitiesByProject(Project project) {
        return artifactVersionRepository.findByProjectVersionProject(project);
    }

    @Override
    public List<ArtifactVersion> retrieveVersionEntitiesByBaseEntity(Artifact artifact) {
        return artifactVersionRepository.findByArtifact(artifact);
    }

    @Override
    public List<Artifact> retrieveBaseEntitiesByProject(Project project) {
        return this.artifactRepository.findByProject(project);
    }

    @Override
    public ArtifactAppEntity retrieveAppEntityFromVersionEntity(ArtifactVersion artifactVersion) {
        // Step 1 - Create base entity information

        ProjectVersion projectVersion = artifactVersion.getProjectVersion();
        TypeReference<Map<String, String>> typeReference = new TypeReference<Map<String, String>>() {
        };
        Map<String, String> customFields = JsonFileUtilities.parse(artifactVersion.getCustomFields(), typeReference);

        ArtifactAppEntity artifactAppEntity =
            new ArtifactAppEntity(artifactVersion.getArtifact().getArtifactId().toString(),
                artifactVersion.getTypeName(),
                artifactVersion.getName(),
                artifactVersion.getSummary(),
                artifactVersion.getContent(),
                artifactVersion.getArtifact().getDocumentType(),
                customFields);

        // Step 2 - Attach document links
        attachDocumentLinks(projectVersion, artifactVersion, artifactAppEntity);

        // Step 3 - Attach Safety Case or FTA information
        attachDocumentNodeInformation(artifactAppEntity, artifactVersion.getArtifact());
        return artifactAppEntity;
    }

    /**
     * Private helper methods
     */

    private void attachDocumentLinks(ProjectVersion projectVersion,
                                     ArtifactVersion artifactVersion,
                                     ArtifactAppEntity artifactAppEntity) {
        Artifact artifact = artifactVersion.getArtifact();
        List<String> documentIds =
            this.documentArtifactRepository
                .findByProjectVersionAndArtifact(projectVersion, artifact)
                .stream()
                .map(da -> da.getDocument().getDocumentId().toString())
                .collect(Collectors.toList());
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
                                           List<String> incomingDocumentIds) {
        List<String> persistedDocumentIds = documentArtifactRepository
            //TODO: Implement document versioning
            .findByProjectVersionProjectAndArtifact(projectVersion.getProject(), artifact)
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

    private Artifact createOrUpdateArtifactFromAppEntity(Project project,
                                                         ArtifactAppEntity artifactAppEntity) throws SafaError {
        String artifactId = artifactAppEntity.getBaseEntityId();
        String typeName = artifactAppEntity.type;
        String artifactName = artifactAppEntity.name;
        ArtifactType artifactType = findOrCreateArtifactType(project, typeName);
        DocumentType documentType = artifactAppEntity.getDocumentType();
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
