package edu.nd.crc.safa.server.controllers;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.server.entities.api.SafaError;
import edu.nd.crc.safa.server.entities.api.ServerResponse;
import edu.nd.crc.safa.server.entities.app.ArtifactAppEntity;
import edu.nd.crc.safa.server.entities.app.VersionMessage;
import edu.nd.crc.safa.server.entities.db.Artifact;
import edu.nd.crc.safa.server.entities.db.Document;
import edu.nd.crc.safa.server.entities.db.DocumentArtifact;
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
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

/**
 * Provides CRUD endpoints for document-artifact relations.
 */
@RestController
public class DocumentArtifactController extends BaseController {

    private final DocumentRepository documentRepository;
    private final ArtifactRepository artifactRepository;
    private final DocumentArtifactRepository documentArtifactRepository;
    private final NotificationService notificationService;

    @Autowired
    public DocumentArtifactController(ProjectRepository projectRepository,
                                      ProjectVersionRepository projectVersionRepository,
                                      DocumentRepository documentRepository,
                                      ArtifactRepository artifactRepository,
                                      DocumentArtifactRepository documentArtifactRepository,
                                      NotificationService notificationService,
                                      ResourceBuilder resourceBuilder) {
        super(projectRepository, projectVersionRepository, resourceBuilder);
        this.documentRepository = documentRepository;
        this.artifactRepository = artifactRepository;
        this.documentArtifactRepository = documentArtifactRepository;
        this.notificationService = notificationService;
    }

    /**
     * Creates associations between each artifact given and the document
     * specified by the documentId.
     *
     * @param versionId  The UUID representing the current version to add the document in.
     * @param documentId The UUID of the document whose artifacts will be added in.
     * @param artifacts  The artifacts to be added to the document.
     * @return List of updated artifact containing document id in series of documents.
     * @throws SafaError Throws error if authorized user does not have edit permission on project
     */
    @PostMapping(AppRoutes.Projects.addArtifactsToDocument)
    public ServerResponse addArtifactToDocuments(@PathVariable UUID versionId,
                                                 @PathVariable UUID documentId,
                                                 @RequestBody List<ArtifactAppEntity> artifacts
    ) throws SafaError {
        ProjectVersion projectVersion = resourceBuilder.fetchVersion(versionId).withEditVersion();
        Document document = getDocumentById(this.documentRepository, documentId);
        for (ArtifactAppEntity a : artifacts) {
            Artifact artifact = getArtifactById(UUID.fromString(a.getId()));
            DocumentArtifact documentArtifact = new DocumentArtifact(projectVersion, document, artifact);
            this.documentArtifactRepository.save(documentArtifact);
            a.addDocumentId(document.getDocumentId().toString());
        }
        return new ServerResponse(artifacts);
    }

    @DeleteMapping(AppRoutes.Projects.removeArtifactFromDocument)
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void removeArtifactFromDocument(@PathVariable UUID versionId,
                                           @PathVariable UUID documentId,
                                           @PathVariable UUID artifactId) throws SafaError {
        ProjectVersion projectVersion = resourceBuilder.fetchVersion(versionId).withEditVersion();
        Document document = getDocumentById(this.documentRepository, documentId);
        Artifact artifact = getArtifactById(artifactId);
        Optional<DocumentArtifact> documentArtifactQuery =
            this.documentArtifactRepository.findByProjectVersionAndDocumentAndArtifact(projectVersion,
                document,
                artifact);
        documentArtifactQuery.ifPresent(this.documentArtifactRepository::delete);
        this.notificationService.broadUpdateProjectVersionMessage(projectVersion, VersionMessage.ARTIFACTS);
    }

    private Artifact getArtifactById(UUID artifactId) throws SafaError {
        Optional<Artifact> artifactOptional = this.artifactRepository.findById(artifactId);
        if (artifactOptional.isPresent()) {
            return artifactOptional.get();
        }
        throw new SafaError("Could not find artifact with id: " + artifactId);
    }
}
