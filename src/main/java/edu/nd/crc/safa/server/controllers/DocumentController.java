package edu.nd.crc.safa.server.controllers;

import java.util.List;
import java.util.UUID;
import javax.validation.Valid;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.common.AppRoutes;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.app.documents.DocumentAppEntity;
import edu.nd.crc.safa.server.entities.app.project.ProjectEntityTypes;
import edu.nd.crc.safa.server.entities.db.Document;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.documents.DocumentRepository;
import edu.nd.crc.safa.server.services.DocumentService;
import edu.nd.crc.safa.server.services.NotificationService;
import edu.nd.crc.safa.server.services.retrieval.AppEntityRetrievalService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

/**
 * Provides CRUD operations for Document entity.
 */
@RestController
public class DocumentController extends BaseController {

    private final DocumentRepository documentRepository;

    private final DocumentService documentService;
    private final NotificationService notificationService;
    private final AppEntityRetrievalService appEntityRetrievalService;

    @Autowired
    public DocumentController(ResourceBuilder resourceBuilder,
                              DocumentRepository documentRepository,
                              DocumentService documentService,
                              NotificationService notificationService,
                              AppEntityRetrievalService appEntityRetrievalService) {
        super(resourceBuilder);
        this.documentRepository = documentRepository;
        this.documentService = documentService;
        this.notificationService = notificationService;
        this.appEntityRetrievalService = appEntityRetrievalService;
    }

    /**
     * Persists given document object as a new document a part of the specified project.
     *
     * @param versionId         The UUID of the project version to who create the document and make
     *                          the artifact additions to.
     * @param documentAppEntity The entity containing name, description, and type of document to be created.
     * @return DocumentAppEntity The updated or created document.
     * @throws SafaError Throws error if authorized user does not have edit permissions.
     */
    @PostMapping(AppRoutes.Projects.Documents.createOrUpdateDocument)
    @ResponseStatus(HttpStatus.CREATED)
    public DocumentAppEntity createOrUpdateDocument(@PathVariable UUID versionId,
                                                    @RequestBody @Valid DocumentAppEntity documentAppEntity)
        throws SafaError {
        ProjectVersion projectVersion = resourceBuilder.fetchVersion(versionId).withEditVersion();
        Project project = projectVersion.getProject();
        documentAppEntity.setProject(project); // Manually set to verify authenticity

        // Create or update: document base entity
        Document document = documentAppEntity.toDocument();
        this.documentRepository.save(document);
        if (documentAppEntity.getDocumentId() == null) {
            documentAppEntity.setDocumentId(document.getDocumentId());
        }

        // Create or update: artifact links
        int nArtifactUpdated = documentService.createOrUpdateArtifactIds(projectVersion, document,
            documentAppEntity.getArtifactIds());

        // Create or update: columns
        documentService.updateFMEAColumns(documentAppEntity, document);

        // Update version subscribers
        documentService.notifyDocumentChanges(projectVersion, nArtifactUpdated > 0);
        return documentAppEntity;
    }


    /**
     * Returns the Documents associated with given specified project.
     *
     * @param projectId The UUID of the project whose documents are returned.
     * @return List of project documents.
     * @throws SafaError Throws error if authorized user does not have permission to view project.
     */
    @GetMapping(AppRoutes.Projects.Documents.getProjectDocuments)
    public List<DocumentAppEntity> getProjectDocuments(@PathVariable UUID projectId) throws SafaError {
        Project project = resourceBuilder.fetchProject(projectId).withViewProject();
        return this.appEntityRetrievalService.getDocumentsInProject(project);
    }

    /**
     * Deletes the document specified by the given id all cascading entities including
     * 1. Document-Artifact Links
     * 2. DocumentColumns
     *
     * @param documentId The UUID of the document to delete.
     * @throws SafaError Throws error is authorized user does not have edit permission.
     */
    @DeleteMapping(AppRoutes.Projects.Documents.deleteDocument)
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteDocument(@PathVariable UUID documentId) throws SafaError {
        Document document = getDocumentById(this.documentRepository, documentId);
        Project project = document.getProject();
        resourceBuilder.setProject(project).withEditProject();
        this.notificationService.broadUpdateProjectMessage(project, ProjectEntityTypes.DOCUMENTS);
        this.documentRepository.delete(document);
    }
}
