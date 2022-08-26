package edu.nd.crc.safa.features.documents.controller;

import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.stream.Collectors;
import javax.validation.Valid;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.documents.entities.app.DocumentAppEntity;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.documents.services.DocumentService;
import edu.nd.crc.safa.features.layout.entities.app.LayoutManager;
import edu.nd.crc.safa.features.layout.entities.app.LayoutPosition;
import edu.nd.crc.safa.features.notifications.builders.EntityChangeBuilder;
import edu.nd.crc.safa.features.notifications.services.NotificationService;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

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
public class DocumentController extends BaseDocumentController {
    private final DocumentService documentService;
    private final NotificationService notificationService;

    @Autowired
    public DocumentController(ResourceBuilder resourceBuilder,
                              ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
        this.documentService = serviceProvider.getDocumentService();
        this.notificationService = serviceProvider.getNotificationService();
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
    @PostMapping(AppRoutes.Documents.CREATE_OR_UPDATE_DOCUMENT)
    @ResponseStatus(HttpStatus.CREATED)
    public DocumentAppEntity createOrUpdateDocument(@PathVariable UUID versionId,
                                                    @RequestBody @Valid DocumentAppEntity documentAppEntity)
        throws SafaError {
        ProjectVersion projectVersion = resourceBuilder.fetchVersion(versionId).withEditVersion();
        Project project = projectVersion.getProject();

        // Create or update: document base entity
        Document document = documentAppEntity.toDocument();
        document.setProject(project);
        this.documentRepository.save(document);

        if (documentAppEntity.getDocumentId() == null) {
            documentAppEntity.setDocumentId(document.getDocumentId());
        }

        // Create or update: artifact links
        documentService.createOrUpdateArtifactIds(
            projectVersion,
            document,
            documentAppEntity.getArtifactIds());
        List<UUID> affectedArtifactIds =
            documentAppEntity.getArtifactIds().stream().collect(Collectors.toList());

        // Create or update: columns
        documentService.updateFMEAColumns(documentAppEntity, document);

        // Generate layout
        Map<UUID, LayoutPosition> documentLayout = createDocumentLayout(projectVersion, documentAppEntity);
        documentAppEntity.setLayout(documentLayout);

        // Update version subscribers
        notificationService.broadcastChange(
            EntityChangeBuilder.create(project.getProjectId())
                .withDocumentUpdate(List.of(document.getDocumentId()))
                .withArtifactsUpdate(affectedArtifactIds)
        );

        return documentAppEntity;
    }

    public Map<UUID, LayoutPosition> createDocumentLayout(ProjectVersion projectVersion,
                                                          DocumentAppEntity documentAppEntity) {
        LayoutManager projectLayout = new LayoutManager(serviceProvider, projectVersion);
        return projectLayout.generateDocumentLayout(documentAppEntity.toDocument(), true);
    }

    /**
     * Returns the Documents associated with given specified project.
     *
     * @param versionId ID of project version used to retrieve layout of document.
     * @return List of project documents.
     * @throws SafaError Throws error if authorized user does not have permission to view project.
     */
    @GetMapping(AppRoutes.Documents.GET_PROJECT_DOCUMENTS)
    public List<DocumentAppEntity> getProjectDocuments(@PathVariable UUID versionId) throws SafaError {
        ProjectVersion projectVersion = resourceBuilder.fetchVersion(versionId).withViewVersion();
        return this.documentService.getAppEntities(projectVersion);
    }

    @GetMapping(AppRoutes.Documents.GET_DOCUMENT_BY_ID)
    public DocumentAppEntity getDocumentById(@PathVariable UUID versionId,
                                             @PathVariable UUID documentId) throws SafaError {
        ProjectVersion projectVersion = this.resourceBuilder.fetchVersion(versionId).withViewVersion();
        Document document = this.documentService.getDocumentById(documentId);
        return this.documentService.createDocumentAppEntity(document, projectVersion);
    }

    /**
     * Deletes the document specified by the given id all cascading entities including
     * 1. Document-Artifact Links
     * 2. DocumentColumns
     *
     * @param documentId The UUID of the document to delete.
     * @throws SafaError Throws error is authorized user does not have edit permission.
     */
    @DeleteMapping(AppRoutes.Documents.DELETE_DOCUMENT_BY_ID)
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteDocument(@PathVariable UUID documentId) throws SafaError {
        // Step - Retrieve document and associated project.
        Document document = getDocumentById(this.documentRepository, documentId);
        Project project = document.getProject();

        // Step - Verify authorized user has permission to delete.
        resourceBuilder.setProject(project).withEditProject();

        // Step - Delete document.
        this.documentRepository.delete(document);

        // Step - Notify project users that document has been deleted.
        this.notificationService.broadcastChange(
            EntityChangeBuilder
                .create(project)
                .withDocumentDelete(documentId)
        );
    }
}
