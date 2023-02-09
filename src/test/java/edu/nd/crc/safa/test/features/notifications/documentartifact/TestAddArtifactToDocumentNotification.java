package edu.nd.crc.safa.test.features.notifications.documentartifact;

import java.util.List;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
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
