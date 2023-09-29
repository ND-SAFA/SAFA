package edu.nd.crc.safa.test.features.notifications.documentartifact;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.List;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.notifications.entities.NotificationEntity;
import edu.nd.crc.safa.test.requests.SafaRequest;

/**
 * Test that whenever an artifact is removed from a document that:
 * - notification is sent to update document and artifacts
 * - default layout is NOT generated
 * - document layout is generated
 */
public class TestRemoveArtifactFromDocumentNotification extends AbstractDocumentArtifactTest {

    /**
     * Creates project, version, document, and artifact not associated with a document.
     *
     * @throws Exception If server error occurs while creating entities.
     */
    @Override
    public void setupTestResources() throws Exception {
        // Step - Create project, version, and document
        super.setupTestResources();

        // Step - Create artifact
        this.testService.createArtifactAndVerifyMessage(this.projectVersion, this);
    }

    @Override
    protected void performAction() throws Exception {
        SafaRequest
            .withRoute(AppRoutes.DocumentArtifact.REMOVE_ARTIFACT_FROM_DOCUMENT)
            .withVersion(projectVersion)
            .withDocument(documentConstants.document)
            .withArtifactId(artifactConstants.artifact.getId())
            .deleteWithJsonObject();
    }

    @Override
    protected void verifyShareeMessage(List<EntityChangeMessage> messages) {
        EntityChangeMessage typeCreationMessage = messages.get(0);
        this.assertionService.verifyArtifactTypeMessage(typeCreationMessage, getArtifact().getType());

        EntityChangeMessage artifactCreationMessage = messages.get(1);
        this.assertionService.verifySingleEntityChanges(artifactCreationMessage,
            List.of(NotificationEntity.ARTIFACTS, NotificationEntity.WARNINGS),
            List.of(1, 0));

        EntityChangeMessage documentUpdateMessage = messages.get(2);
        this.assertionService.verifySingleEntityChanges(documentUpdateMessage,
            List.of(NotificationEntity.DOCUMENT, NotificationEntity.ARTIFACTS),
            List.of(1, 1));
        assertThat(documentUpdateMessage.isUpdateLayout()).isFalse();
    }
}
