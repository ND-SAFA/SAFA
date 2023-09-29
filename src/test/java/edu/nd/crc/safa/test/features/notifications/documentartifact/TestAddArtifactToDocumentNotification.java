package edu.nd.crc.safa.test.features.notifications.documentartifact;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.util.List;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.notifications.entities.NotificationEntity;
import edu.nd.crc.safa.test.requests.SafaRequest;

/**
 * Test that whenever an artifact is added to a document that:
 * - notification is sent to update document and artifacts
 * - default layout is NOT generated
 * - document layout is generated
 */
public class TestAddArtifactToDocumentNotification extends AbstractDocumentArtifactTest {

    @Override
    public void setupTestResources() throws Exception {
        // Step - Create project, version, and document
        super.setupTestResources();
        // Step - Create artifact and verifies notification message
        testService.createArtifactAndVerifyMessage(this.projectVersion, this);
    }

    @Override
    protected void performAction() throws Exception {
        SafaRequest
            .withRoute(AppRoutes.DocumentArtifact.ADD_ARTIFACTS_TO_DOCUMENT)
            .withVersion(projectVersion)
            .withDocument(documentConstants.document)
            .postWithJsonArray(List.of(artifactConstants.artifact));
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
