package edu.nd.crc.safa.features.documents.controller;

import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;

import edu.nd.crc.safa.authentication.builders.ResourceBuilder;
import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.artifacts.entities.ArtifactAppEntity;
import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.artifacts.repositories.ArtifactRepository;
import edu.nd.crc.safa.features.common.ServiceProvider;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.documents.entities.db.DocumentArtifact;
import edu.nd.crc.safa.features.documents.repositories.DocumentArtifactRepository;
import edu.nd.crc.safa.features.layout.entities.app.LayoutManager;
import edu.nd.crc.safa.features.notifications.builders.EntityChangeBuilder;
import edu.nd.crc.safa.features.notifications.services.NotificationService;
import edu.nd.crc.safa.features.permissions.entities.ProjectPermission;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

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
public class DocumentArtifactController extends BaseDocumentController {

    private final ArtifactRepository artifactRepository;
    private final DocumentArtifactRepository documentArtifactRepository;
    private final NotificationService notificationService;

    @Autowired
    public DocumentArtifactController(ResourceBuilder resourceBuilder,
                                      ServiceProvider serviceProvider) {
        super(resourceBuilder, serviceProvider);
        this.artifactRepository = serviceProvider.getArtifactRepository();
        this.documentArtifactRepository = serviceProvider.getDocumentArtifactRepository();
        this.notificationService = serviceProvider.getNotificationService();
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
    @PostMapping(AppRoutes.DocumentArtifact.ADD_ARTIFACTS_TO_DOCUMENT)
    public List<ArtifactAppEntity> addArtifactToDocuments(@PathVariable UUID versionId,
                                                          @PathVariable UUID documentId,
                                                          @RequestBody List<ArtifactAppEntity> artifacts
    ) {
        SafaUser user = getServiceProvider().getSafaUserService().getCurrentUser();
        ProjectVersion projectVersion = getResourceBuilder().fetchVersion(versionId)
                .withPermission(ProjectPermission.EDIT, user).get();
        Document document = getDocumentById(getDocumentRepository(), documentId);
        for (ArtifactAppEntity a : artifacts) {
            UUID artifactId = a.getId();
            Artifact artifact = getArtifactById(artifactId);
            DocumentArtifact documentArtifact = new DocumentArtifact(projectVersion, document, artifact);
            this.documentArtifactRepository.save(documentArtifact);
            a.addDocumentId(document.getDocumentId());
        }

        LayoutManager layoutManager = new LayoutManager(getServiceProvider(), projectVersion, user);
        layoutManager.generateDocumentLayout(document);
        List<UUID> artifactIds = artifacts
            .stream()
            .map(ArtifactAppEntity::getId)
            .collect(Collectors.toList());

        this.notificationService.broadcastChange(
            EntityChangeBuilder
                .create(versionId)
                .withDocumentUpdate(List.of(documentId))
                .withArtifactsUpdate(artifactIds)
        );
        return artifacts;
    }

    @DeleteMapping(AppRoutes.DocumentArtifact.REMOVE_ARTIFACT_FROM_DOCUMENT)
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void removeArtifactFromDocument(@PathVariable UUID versionId,
                                           @PathVariable UUID documentId,
                                           @PathVariable UUID artifactId) {
        SafaUser user = getServiceProvider().getSafaUserService().getCurrentUser();
        ProjectVersion projectVersion = getResourceBuilder().fetchVersion(versionId)
                .withPermission(ProjectPermission.EDIT, user).get();
        Document document = getDocumentById(getDocumentRepository(), documentId);
        Artifact artifact = getArtifactById(artifactId);
        Optional<DocumentArtifact> documentArtifactQuery =
            this.documentArtifactRepository.findByProjectVersionAndDocumentAndArtifact(projectVersion,
                document,
                artifact);
        documentArtifactQuery.ifPresent(this.documentArtifactRepository::delete);

        this.notificationService.broadcastChange(
            EntityChangeBuilder.create(versionId)
                .withDocumentUpdate(List.of(documentId))
                .withArtifactsUpdate(List.of(artifactId))
        );
    }

    private Artifact getArtifactById(UUID artifactId) throws SafaError {
        Optional<Artifact> artifactOptional = this.artifactRepository.findById(artifactId);
        if (artifactOptional.isPresent()) {
            return artifactOptional.get();
        }
        throw new SafaError("Could not find artifact with id: %s", artifactId);
    }
}
