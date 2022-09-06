package features.notifications.documentartifact;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;

import requests.SafaRequest;

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
    protected void verifyShareeMessage(EntityChangeMessage message) {
        this.changeMessageVerifies.verifyDocumentChange(message,
            this.documentId,
            Change.Action.UPDATE);
        this.changeMessageVerifies.verifyArtifactMessage(
            message,
            this.artifactId,
            Change.Action.UPDATE);
        this.changeMessageVerifies.verifyUpdateLayout(message, false);
    }
}
