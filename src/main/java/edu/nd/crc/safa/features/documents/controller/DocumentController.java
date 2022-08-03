package edu.nd.crc.safa.features.documents.controller;

import java.util.List;
import java.util.Map;
import java.util.UUID;
import javax.validation.Valid;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.documents.entities.app.DocumentAppEntity;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.documents.repositories.DocumentRepository;
import edu.nd.crc.safa.features.documents.services.DocumentService;
import edu.nd.crc.safa.features.layout.entities.LayoutPosition;
import edu.nd.crc.safa.features.layout.services.LayoutService;
import edu.nd.crc.safa.features.notifications.NotificationService;
import edu.nd.crc.safa.features.projects.entities.app.ProjectAppEntity;
import edu.nd.crc.safa.features.projects.entities.app.ProjectEntityTypes;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.projects.entities.db.Project;
import edu.nd.crc.safa.features.projects.services.AppEntityRetrievalService;
import edu.nd.crc.safa.features.versions.entities.db.ProjectVersion;

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
    private final AppEntityRetrievalService appEntityRetrievalService;
    private final LayoutService layoutService;

    @Autowired
    public DocumentController(ResourceBuilder resourceBuilder,
                              DocumentRepository documentRepository,
                              DocumentService documentService,
                              NotificationService notificationService,
                              AppEntityRetrievalService appEntityRetrievalService,
                              LayoutService layoutService) {
        super(resourceBuilder, documentRepository);
        this.documentService = documentService;
        this.notificationService = notificationService;
        this.appEntityRetrievalService = appEntityRetrievalService;
        this.layoutService = layoutService;
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
    @PostMapping(AppRoutes.Projects.Documents.CREATE_OR_UPDATE_DOCUMENT)
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
        int nArtifactUpdated = documentService.createOrUpdateArtifactIds(
            projectVersion,
            document,
            documentAppEntity.getArtifactIds());

        // Create or update: columns
        documentService.updateFMEAColumns(documentAppEntity, document);

        // Update version subscribers
        documentService.notifyDocumentChanges(projectVersion, nArtifactUpdated > 0);

        // Generate layout
        Map<String, LayoutPosition> documentLayout = createDocumentLayout(projectVersion, documentAppEntity);
        documentAppEntity.setLayout(documentLayout);

        return documentAppEntity;
    }

    public Map<String, LayoutPosition> createDocumentLayout(ProjectVersion projectVersion,
                                                            DocumentAppEntity documentAppEntity) {
        ProjectAppEntity projectAppEntity =
            this.appEntityRetrievalService.retrieveProjectAppEntityAtProjectVersion(projectVersion);
        //TODO: Replace with layout retrieval.
        Map<String, Map<String, LayoutPosition>> documentLayoutMap =
            this.layoutService.generateDocumentLayouts(projectAppEntity.artifacts,
                projectAppEntity.traces,
                List.of(documentAppEntity));
        return documentLayoutMap.get(documentAppEntity.getDocumentId().toString());
    }


    /**
     * Returns the Documents associated with given specified project.
     *
     * @param projectId The UUID of the project whose documents are returned.
     * @return List of project documents.
     * @throws SafaError Throws error if authorized user does not have permission to view project.
     */
    @GetMapping(AppRoutes.Projects.Documents.GET_PROJECT_DOCUMENTS)
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
    @DeleteMapping(AppRoutes.Projects.Documents.DELETE_DOCUMENT)
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteDocument(@PathVariable UUID documentId) throws SafaError {
        Document document = getDocumentById(this.documentRepository, documentId);
        Project project = document.getProject();
        resourceBuilder.setProject(project).withEditProject();
        this.notificationService.broadUpdateProjectMessage(project, ProjectEntityTypes.DOCUMENTS);
        this.documentRepository.delete(document);
    }
}
