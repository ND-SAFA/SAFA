package edu.nd.crc.safa.test.features.notifications.documentartifact;

import java.util.List;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.test.requests.SafaRequest;

/**
 * Test that whenever an artifact is removed from a document that:
 * - notification is sent to update document and artifacts
 * - default layout is NOT generated
 * - document layout is generated
 */
public class TestNotificationOnRemoveArtifactFromDocument extends AbstractDocumentArtifactTest {

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
        this.rootBuilder
            .store(s -> s
                .save("version", this.projectVersion))
            .and()
            .actions((s, a) -> a
                .createArtifactAndVerifyMessage(s.getProjectVersion("version"), this));
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
    protected void verifyShareeMessages(List<EntityChangeMessage> messages) {
        EntityChangeMessage message = messages.get(0);
        this.rootBuilder.verify(v -> v.notifications(n -> n.verifyDocumentChangeMessage(message)));
    }
}
