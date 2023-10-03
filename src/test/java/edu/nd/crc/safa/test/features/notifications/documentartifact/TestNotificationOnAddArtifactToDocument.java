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
    protected void verifyShareeMessage(List<EntityChangeMessage> messages) {
        EntityChangeMessage typeCreationMessage = messages.get(0);
        this.rootBuilder
            .verify(v -> v.notifications(n -> n
                .verifyArtifactTypeMessage(typeCreationMessage, getArtifact().getType())));

        EntityChangeMessage artifactCreationMessage = messages.get(1);
        this.rootBuilder
            .verify(v -> v
                .notifications(n -> n
                    .verifySingleEntityChanges(artifactCreationMessage,
                        List.of(NotificationEntity.ARTIFACTS, NotificationEntity.WARNINGS),
                        List.of(1, 0))));

        EntityChangeMessage documentUpdateMessage = messages.get(2);
        this
            .rootBuilder
            .verify(v -> v
                .notifications(n -> n
                    .verifySingleEntityChanges(documentUpdateMessage,
                        List.of(NotificationEntity.DOCUMENT, NotificationEntity.ARTIFACTS),
                        List.of(1, 1))));
        assertThat(documentUpdateMessage.isUpdateLayout()).isFalse();
    }
}
