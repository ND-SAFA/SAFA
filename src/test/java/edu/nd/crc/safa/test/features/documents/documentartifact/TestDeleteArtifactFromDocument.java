package edu.nd.crc.safa.test.features.documents.documentartifact;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.artifacts.entities.db.Artifact;
import edu.nd.crc.safa.features.documents.entities.db.Document;
import edu.nd.crc.safa.features.documents.entities.db.DocumentArtifact;
import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.notifications.entities.NotificationAction;
import edu.nd.crc.safa.features.notifications.entities.NotificationEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;
import edu.nd.crc.safa.test.common.ApplicationBaseTest;
import edu.nd.crc.safa.test.common.EntityConstants;
import edu.nd.crc.safa.test.requests.RouteBuilder;
import edu.nd.crc.safa.test.requests.SafaRequest;

import org.junit.jupiter.api.Test;

/**
 * Tests that the client is able to remove an artifact from a document
 */
class TestDeleteArtifactFromDocument extends ApplicationBaseTest {

    EntityConstants.DocumentConstants documentConstants = new EntityConstants.DocumentConstants();
    EntityConstants.ArtifactConstants artifactConstants = new EntityConstants.ArtifactConstants();

    /**
     * Verifies that:
     * - Client is able to remove user from document
     * - Other members are notified that member has been removed.
     */
    @Test
    void testDeleteArtifactFromDocument() throws Exception {
        // Step - Create, project, document, three artifact
        ProjectVersion projectVersion = createProjectData();
        Document document = dbEntityBuilder.getDocument(projectName, documentConstants.name);
        Artifact artifact = dbEntityBuilder.getArtifact(projectName, artifactConstants.name);

        // VP - Verify that artifact is linked
        Optional<DocumentArtifact> documentArtifactOptional = this.documentArtifactRepository
            .findByProjectVersionAndDocumentAndArtifact(projectVersion, document, artifact);
        assertThat(documentArtifactOptional).isPresent();

        // Step - Subscribe to version updates as other member
        notificationService.initializeUser(currentUser, this.token);
        notificationService.subscribeToProject(currentUser, projectVersion.getProject());
        notificationService.subscribeToVersion(currentUser, projectVersion);

        this.assertionService.verifyActiveMembers(List.of(currentUser), this.notificationService);

        // Step - Request artifact is removed from document
        String route = RouteBuilder
            .withRoute(AppRoutes.DocumentArtifact.REMOVE_ARTIFACT_FROM_DOCUMENT)
            .withVersion(projectVersion)
            .withDocument(document)
            .withArtifactId(artifact)
            .buildEndpoint();
        SafaRequest.withRoute(route).deleteWithJsonObject();

        // VP - Verify that artifact is no longer linked
        List<DocumentArtifact> documentArtifactList = this.documentArtifactRepository.findByDocument(document);
        assertThat(documentArtifactList).isEmpty();

        // VP - Verify that 2 changes are detected (document + artifacts).
        EntityChangeMessage message = notificationService.getEntityMessage(currentUser); //TODO: fails on rare occasions
        assertThat(message.getChanges()).hasSize(2);

        // VP - Verify that change is for a deleted member
        List<NotificationEntity> changedEntities =
            message.getChanges().stream().map(Change::getEntity).collect(Collectors.toList());
        Change change = message.getChanges().get(0);
        assertThat(changedEntities)
            .contains(NotificationEntity.DOCUMENT)
            .contains(NotificationEntity.ARTIFACTS);

        // VP - Verify document change has action: UPDATE
        Change documentChange = message.getChangeForEntity(NotificationEntity.DOCUMENT);
        assertThat(documentChange.getAction()).isEqualTo(NotificationAction.UPDATE);
        assertThat(documentChange.getEntityIds()).hasSize(1);

        // VP - Verify that artifact change has action: UPDATE
        Change artifactChange = message.getChangeForEntity(NotificationEntity.ARTIFACTS);
        assertThat(artifactChange.getAction()).isEqualTo(NotificationAction.UPDATE);
        assertThat(artifactChange.getEntityIds()).hasSize(1);
    }

    public ProjectVersion createProjectData() {
        return dbEntityBuilder
            .newProject(projectName)
            .newVersion(projectName)
            .newType(projectName, artifactConstants.type)
            .newArtifactAndBody(projectName,
                artifactConstants.type,
                artifactConstants.name,
                artifactConstants.summary,
                artifactConstants.body)
            .newDocument(projectName,
                documentConstants.name,
                documentConstants.description,
                documentConstants.type)
            .newDocumentArtifact(projectName, 0, documentConstants.name, artifactConstants.name)
            .getProjectVersion(projectName, 0);
    }

}
