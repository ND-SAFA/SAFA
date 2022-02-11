package edu.nd.crc.safa.server.controllers;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;
import javax.validation.Valid;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.api.DocumentAppEntity;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.api.ServerResponse;
import edu.nd.crc.safa.server.entities.app.ProjectMessage;
import edu.nd.crc.safa.server.entities.app.VersionMessage;
import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.Document;
import edu.nd.crc.safa.server.entities.db.DocumentArtifact;
import edu.nd.crc.safa.server.entities.db.Project;
import edu.nd.crc.safa.server.entities.db.ProjectVersion;
import edu.nd.crc.safa.server.repositories.ArtifactRepository;
import edu.nd.crc.safa.server.repositories.DocumentArtifactRepository;
import edu.nd.crc.safa.server.repositories.DocumentRepository;
import edu.nd.crc.safa.server.repositories.ProjectRepository;
import edu.nd.crc.safa.server.repositories.ProjectVersionRepository;
import edu.nd.crc.safa.server.services.NotificationService;

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
    private final ArtifactRepository artifactRepository;
    private final DocumentArtifactRepository documentArtifactRepository;

    private final NotificationService notificationService;

    @Autowired
    public DocumentController(ProjectRepository projectRepository,
                              ProjectVersionRepository projectVersionRepository,
                              ResourceBuilder resourceBuilder,
                              DocumentRepository documentRepository,
                              ArtifactRepository artifactRepository,
                              DocumentArtifactRepository documentArtifactRepository,
                              NotificationService notificationService) {
        super(projectRepository, projectVersionRepository, resourceBuilder);
        this.documentRepository = documentRepository;
        this.artifactRepository = artifactRepository;
        this.documentArtifactRepository = documentArtifactRepository;
        this.notificationService = notificationService;
    }

    /**
     * Persists given document object as a new document a part of the specified project.
     *
     * @param versionId         The UUID of the project version to who create the document and make
     *                          the artifact additions to.
     * @param documentAppEntity The entity containing name, description, and type of document to be created.
     * @return The updated or created document.
     * @throws SafaError Throws error if authorized user does not have edit permissions.
     */
    @PostMapping(AppRoutes.Projects.createOrUpdateDocument)
    @ResponseStatus(HttpStatus.CREATED)
    public ServerResponse createOrUpdateDocument(@PathVariable UUID versionId,
                                                 @RequestBody @Valid DocumentAppEntity documentAppEntity)
        throws SafaError {
        ProjectVersion projectVersion = resourceBuilder.fetchVersion(versionId).withEditVersion();
        Project project = projectVersion.getProject();
        documentAppEntity.setProject(projectVersion.getProject());

        System.out.println("START");
        Document document = documentAppEntity.toDocument();
        this.documentRepository.save(document);
        documentAppEntity.setDocumentId(document.getDocumentId());
        this.createDocumentArtifactEntities(projectVersion, documentAppEntity.getArtifactIds(), document);
        System.out.println("END");

        this.notificationService.broadUpdateProjectMessage(project, ProjectMessage.DOCUMENTS);
        if (documentAppEntity.getArtifactIds().size() > 0) {
            this.notificationService.broadUpdateProjectVersionMessage(projectVersion, VersionMessage.ARTIFACTS);
        }
        return new ServerResponse(documentAppEntity);
    }

    /**
     * Returns the Documents associated with given specified project.
     *
     * @param projectId The UUID of the project whose documents are returned.
     * @return List of project documents.
     * @throws SafaError Throws error if authorized user does not have permission to view project.
     */
    @GetMapping(AppRoutes.Projects.getProjectDocuments)
    public ServerResponse getProjectDocuments(@PathVariable UUID projectId) throws SafaError {
        Project project = resourceBuilder.fetchProject(projectId).withViewProject();
        List<Document> projectDocuments = this.documentRepository.findByProject(project);
        List<DocumentAppEntity> documentAppEntities = new ArrayList<>();
        for (Document document : projectDocuments) {
            List<String> artifactIds = this.documentArtifactRepository.findByDocument(document)
                .stream()
                .map(da -> da.getArtifact().getArtifactId().toString())
                .collect(Collectors.toList());
            DocumentAppEntity documentAppEntity = new DocumentAppEntity(document, artifactIds);
            documentAppEntities.add(documentAppEntity);

        }
        return new ServerResponse(documentAppEntities);
    }

    /**
     * Deletes the document specified by the given id.
     *
     * @param documentId The UUID of the document to delete.
     * @throws SafaError Throws error is authorized user does not have edit permission.
     */
    @DeleteMapping(AppRoutes.Projects.deleteDocument)
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteDocument(@PathVariable UUID documentId) throws SafaError {
        Document document = getDocumentById(this.documentRepository, documentId);
        Project project = document.getProject();
        resourceBuilder.setProject(project).withEditProject();
        this.notificationService.broadUpdateProjectMessage(project, ProjectMessage.DOCUMENTS);
        this.documentRepository.delete(document);
    }

    private void createDocumentArtifactEntities(ProjectVersion projectVersion,
                                                List<String> artifactIds,
                                                Document document) {
        List<UUID> artifactUUIDs = artifactIds
            .stream()
            .map(UUID::fromString)
            .collect(Collectors.toList());
        for (UUID artifactId : artifactUUIDs) {
            Optional<Artifact> artifactOptional = this.artifactRepository.findById(artifactId);
            if (artifactOptional.isPresent()) {
                Artifact artifact = artifactOptional.get();
                DocumentArtifact documentArtifact = new DocumentArtifact(projectVersion, document, artifact);
                this.documentArtifactRepository.save(documentArtifact);
            }
        }
    }
}
