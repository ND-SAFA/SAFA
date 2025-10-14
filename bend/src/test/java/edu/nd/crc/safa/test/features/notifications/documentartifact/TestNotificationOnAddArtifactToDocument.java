package edu.nd.crc.safa.test.features.notifications.documentartifact;


import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.test.requests.SafaRequest;

/**
 * Test that whenever an artifact is added to a document that:
 * - notification is sent to update document and artifacts
 * - default layout is NOT generated
 * - document layout is generated
 */
public class TestNotificationOnAddArtifactToDocument extends AbstractDocumentArtifactTest {

    @Override
    public void setupTestResources() throws Exception {
        // Step - Create project, version, and document
        super.setupTestResources();
        // Step - Create artifact and verifies notification message
        this.rootBuilder
            .store(s -> s.save("version", this.projectVersion))
            .and().actions((s, a) -> a
                .createArtifactAndVerifyMessage(s.getProjectVersion("version"), this));
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
    protected void verifyShareeMessages(List<EntityChangeMessage> messages) {
        assertThat(messages).hasSize(1);
        EntityChangeMessage message = messages.get(0);
        this.rootBuilder.verify(v -> v.notifications(n -> n.verifyDocumentChangeMessage(message)));
    }
}
