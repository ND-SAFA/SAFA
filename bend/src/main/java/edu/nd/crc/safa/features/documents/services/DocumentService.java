package edu.nd.crc.safa.features.documents.services;

import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactRepository;
import edu.nd.crc.safa.features.artifacts.services.ArtifactService;
import edu.nd.crc.safa.features.common.IAppEntityService;
import edu.nd.crc.safa.features.documents.entities.app.DocumentAppEntity;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.documents.entities.db.DocumentArtifact;
import edu.nd.crc.safa.features.documents.repositories.DocumentArtifactRepository;
import edu.nd.crc.safa.features.documents.repositories.DocumentRepository;
import edu.nd.crc.safa.features.layout.entities.app.LayoutPosition;
import edu.nd.crc.safa.features.layout.services.ArtifactPositionService;
import edu.nd.crc.safa.features.notifications.builders.EntityChangeBuilder;
import edu.nd.crc.safa.features.notifications.services.NotificationService;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.app.SafaItemNotFoundError;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

/**
 * Responsible for coordinating the creations and updates to a DocumentAppEntity
 * and its related fields.
 */
@Service
@AllArgsConstructor
public class DocumentService implements IAppEntityService<DocumentAppEntity> {

    private final DocumentRepository documentRepository;
    private final ArtifactRepository artifactRepository;
    private final DocumentArtifactRepository documentArtifactRepository;
    private final ArtifactPositionService artifactPositionService;
    private final ArtifactService artifactService;
    private final NotificationService notificationService;

    /**
     * Returns list of documents in given project
     *
     * @param projectVersion The version used to calculate artifact positions within the document.
     * @param user           The user making the request
     * @return List of documents in project.
     */
    @Override
    public List<DocumentAppEntity> getAppEntities(ProjectVersion projectVersion, SafaUser user) {
        return this.documentRepository.findByProject(projectVersion.getProject())
            .stream()
            .map(d -> createDocumentAppEntity(d, projectVersion))
            .collect(Collectors.toList());
    }

    @Override
    public List<DocumentAppEntity> getAppEntitiesByIds(ProjectVersion projectVersion, SafaUser user,
                                                       List<UUID> appEntityIds) {
        return this.documentRepository.findByProjectAndDocumentIdIn(projectVersion.getProject(), appEntityIds)
            .stream()
            .map(d -> createDocumentAppEntity(d, projectVersion))
            .collect(Collectors.toList());
    }

    /**
     * Compares the artifacts linked to document with the one's given and creates / deletes links as necessary.
     *
     * @param projectVersion The project version associated with the link between artifact and document.
     * @param document       The document whose artifact ids are being updated.
     * @param artifactIds    The artifactIds that should represent the artifact ids in the document at the given project
     *                       version.
     * @return The number of artifact entities updated.
     * @throws SafaError Throws error if an artifactId does not exist in system.
     */
    public int createOrUpdateArtifactIds(ProjectVersion projectVersion,
                                         Document document,
                                         List<UUID> artifactIds) throws SafaError {
        List<DocumentArtifact> documentArtifacts = this.documentArtifactRepository.findByDocument(document);
        List<UUID> artifactIdsLinkedToDocument = documentArtifacts
            .stream()
            .map(da -> da.getArtifact().getArtifactId())
            .collect(Collectors.toList());
        int nUpdated = 0;

        nUpdated += createNewDocumentArtifactLinks(projectVersion, document, artifactIds, artifactIdsLinkedToDocument);
        nUpdated += removeDeletedDocumentArtifactLinks(document, artifactIds, artifactIdsLinkedToDocument);
        return nUpdated;
    }

    private int removeDeletedDocumentArtifactLinks(Document document,
                                                   List<UUID> artifactIds,
                                                   List<UUID> artifactIdsLinkedToDocument) {
        int nUpdated = 0;
        for (UUID linkedArtifactId : artifactIdsLinkedToDocument) {
            if (!artifactIds.contains(linkedArtifactId)) {
                Optional<DocumentArtifact> documentArtifactOptional =
                    this.documentArtifactRepository.findByDocumentAndArtifactArtifactId(document,
                        linkedArtifactId);
                if (documentArtifactOptional.isPresent()) {
                    DocumentArtifact documentArtifact = documentArtifactOptional.get();
                    this.documentArtifactRepository.delete(documentArtifact);
                    nUpdated++;
                }
            }
        }
        return nUpdated;
    }

    private int createNewDocumentArtifactLinks(ProjectVersion projectVersion,
                                               Document document,
                                               List<UUID> artifactIds,
                                               List<UUID> artifactIdsLinkedToDocument) throws SafaError {
        int nUpdated = 0;
        for (UUID artifactId : artifactIds) {
            if (!artifactIdsLinkedToDocument.contains(artifactId)) {
                Optional<Artifact> artifactOptional = this.artifactRepository.findById(artifactId);
                if (artifactOptional.isPresent()) {
                    Artifact artifact = artifactOptional.get();
                    DocumentArtifact documentArtifact = new DocumentArtifact(
                        projectVersion,
                        document,
                        artifact
                    );
                    this.documentArtifactRepository.save(documentArtifact);
                    nUpdated++;
                } else {
                    throw new SafaError("Could not find artifact with id: %s", artifactId);
                }

            }
        }
        return nUpdated;
    }

    /**
     * Creates {@link DocumentAppEntity} from its database entity {@link Document}.
     * This includes retrieving linked artifacts and their positions
     *
     * @param document       Persisted document base entity.
     * @param projectVersion The version of the document's artifact to generate layout with.
     * @return {@link DocumentAppEntity} Representing front-end model of document.
     */
    public DocumentAppEntity createDocumentAppEntity(Document document, ProjectVersion projectVersion) {
        // Step - Retrieve linked artifact Ids
        List<UUID> artifactIds = this.documentArtifactRepository.findByDocument(document)
            .stream()
            .map(da -> da.getArtifact().getArtifactId())
            .collect(Collectors.toList());

        // Step - Retrieve artifact layout
        Map<UUID, LayoutPosition> documentLayout =
            this.artifactPositionService.retrieveDocumentLayout(projectVersion, document.getDocumentId());

        // Step - Create document app entity

        return new DocumentAppEntity(document, artifactIds, documentLayout);
    }

    public Document getDocumentById(UUID documentId) {
        Optional<Document> documentOptional = this.documentRepository.findById(documentId);
        if (documentOptional.isPresent()) {
            return documentOptional.get();
        } else {
            throw new SafaItemNotFoundError("Could not find document with id:" + documentId);
        }
    }

    public void broadcastDocumentChange(SafaUser user, ProjectVersion projectVersion, Document document,
                                        List<UUID> removedArtifactIds) {
        DocumentAppEntity documentAppEntity = this.createDocumentAppEntity(document, projectVersion);
        List<UUID> documentArtifactIds = documentAppEntity.getArtifactIds();
        documentArtifactIds.addAll(removedArtifactIds); // Artifacts updates with new relationships to documents.
        List<ArtifactAppEntity> documentArtifacts = artifactService
            .getAppEntitiesByIds(projectVersion, documentAppEntity.getArtifactIds());
        this.notificationService.broadcastChange(
            EntityChangeBuilder
                .create(user, projectVersion)
                .withDocumentUpdate(List.of(documentAppEntity))
                .withArtifactsUpdate(documentArtifacts)
        );
    }
}
