package edu.nd.crc.safa.features.documents.services;

import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactRepository;
import edu.nd.crc.safa.features.documents.entities.app.DocumentAppEntity;
import edu.nd.crc.safa.features.documents.entities.app.DocumentColumnAppEntity;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.documents.entities.db.DocumentArtifact;
import edu.nd.crc.safa.features.documents.entities.db.DocumentColumn;
import edu.nd.crc.safa.features.documents.entities.db.DocumentType;
import edu.nd.crc.safa.features.documents.repositories.DocumentArtifactRepository;
import edu.nd.crc.safa.features.documents.repositories.DocumentColumnRepository;
import edu.nd.crc.safa.features.documents.repositories.DocumentRepository;
import edu.nd.crc.safa.features.notifications.NotificationService;
import edu.nd.crc.safa.features.projects.entities.app.ProjectEntityTypes;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.app.VersionEntityTypes;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

/**
 * Responsible for coordinating the creations and updates to a DocumentAppEntity
 * and its related fields.
 */
@Service
@AllArgsConstructor
public class DocumentService {

    private final DocumentRepository documentRepository;
    private final ArtifactRepository artifactRepository;
    private final DocumentArtifactRepository documentArtifactRepository;
    private final DocumentColumnRepository documentColumnRepository;
    private final NotificationService notificationService;

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
                                         List<String> artifactIds) throws SafaError {
        List<DocumentArtifact> documentArtifacts = this.documentArtifactRepository.findByDocument(document);
        List<String> artifactIdsLinkedToDocument = documentArtifacts
            .stream()
            .map(da -> da.getArtifact().getArtifactId().toString())
            .collect(Collectors.toList());
        int nUpdated = 0;

        nUpdated += createNewDocumentArtifactLinks(projectVersion, document, artifactIds, artifactIdsLinkedToDocument);
        nUpdated += removeDeletedDocumentArtifactLinks(document, artifactIds, artifactIdsLinkedToDocument);
        return nUpdated;
    }

    /**
     * If type if FMEA, creates or updates columns
     *
     * @param documentAppEntity The app entity whose columns are persisted.
     * @param document          The document db entity associated with document app entity.
     */
    public void updateFMEAColumns(DocumentAppEntity documentAppEntity, Document document) {
        // Step - Remove columns no longer present in payload
        List<UUID> originalColumnIds = this.documentColumnRepository
            .findByDocument(document)
            .stream()
            .map(DocumentColumn::getDocumentColumnId)
            .collect(Collectors.toList());

        // Step - Add or update column database entities
        if (document.getType() == DocumentType.FMEA) {
            List<DocumentColumnAppEntity> documentColumns = documentAppEntity.getColumns();
            for (int columnIndex = 0; columnIndex < documentColumns.size(); columnIndex++) {
                DocumentColumnAppEntity documentColumnAppEntity = documentColumns.get(columnIndex);
                DocumentColumn documentColumn = new DocumentColumn(
                    documentColumnAppEntity,
                    document,
                    columnIndex);
                this.documentColumnRepository.save(documentColumn);
                documentAppEntity.getColumns().get(columnIndex).setId(documentColumn.getDocumentColumnId());

                // Mark as processed
                UUID currentColumnId = documentColumn.getDocumentColumnId();
                originalColumnIds.remove(currentColumnId);
            }
        }

        // Step - Remove columns not included in payload
        for (UUID removedColumnId : originalColumnIds) {
            this.documentColumnRepository.deleteById(removedColumnId);
        }
    }

    /**
     * Sends notification to project subscribers that the documents have changed. If updateArtifacts is
     * true then project version subscribers will be notified to update their artifacts.
     *
     * @param projectVersion  The project version whose artifacts are updated.
     * @param updateArtifacts Whether to notify project version subsribers.
     */
    public void notifyDocumentChanges(ProjectVersion projectVersion, boolean updateArtifacts) {
        this.notificationService.broadUpdateProjectMessage(projectVersion.getProject(), ProjectEntityTypes.DOCUMENTS);
        if (updateArtifacts) {
            this.notificationService.broadUpdateProjectVersionMessage(projectVersion, VersionEntityTypes.ARTIFACTS);
        }
    }

    private int removeDeletedDocumentArtifactLinks(Document document,
                                                   List<String> artifactIds,
                                                   List<String> artifactIdsLinkedToDocument) {
        int nUpdated = 0;
        for (String linkedArtifactId : artifactIdsLinkedToDocument) {
            if (!artifactIds.contains(linkedArtifactId)) {
                Optional<DocumentArtifact> documentArtifactOptional =
                    this.documentArtifactRepository.findByDocumentAndArtifactArtifactId(document,
                        UUID.fromString(linkedArtifactId));
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
                                               List<String> artifactIds,
                                               List<String> artifactIdsLinkedToDocument) throws SafaError {
        int nUpdated = 0;
        for (String artifactId : artifactIds) {
            if (!artifactIdsLinkedToDocument.contains(artifactId)) {
                Optional<Artifact> artifactOptional = this.artifactRepository.findById(UUID.fromString(artifactId));
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
                    throw new SafaError("Could not find artifact with id: " + artifactId);
                }

            }
        }
        return nUpdated;
    }

    /**
     * Returns list of documents in given project
     *
     * @param project The projects whose documents are returned.
     * @return List of documents in project.
     */
    public List<DocumentAppEntity> getDocumentsInProject(Project project) {
        List<Document> projectDocuments = this.documentRepository.findByProject(project);
        List<DocumentAppEntity> documentAppEntities = new ArrayList<>();
        for (Document document : projectDocuments) {
            // Retrieve linked artifact Ids
            List<String> artifactIds = this.documentArtifactRepository.findByDocument(document)
                .stream()
                .map(da -> da.getArtifact().getArtifactId().toString())
                .collect(Collectors.toList());
            //TODO: Retrieve artifact positions
            DocumentAppEntity documentAppEntity = new DocumentAppEntity(document, artifactIds, new Hashtable<>());

            // Retrieve FMEA columns
            if (document.getType() == DocumentType.FMEA) {
                List<DocumentColumnAppEntity> documentColumns = this.documentColumnRepository
                    .findByDocumentOrderByTableColumnIndexAsc(document)
                    .stream()
                    .map(DocumentColumnAppEntity::new)
                    .collect(Collectors.toList());
                documentAppEntity.setColumns(documentColumns);
            }

            documentAppEntities.add(documentAppEntity);
        }
        return documentAppEntities;
    }
}
