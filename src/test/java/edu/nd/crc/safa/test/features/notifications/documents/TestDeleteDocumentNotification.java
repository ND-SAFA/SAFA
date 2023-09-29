package edu.nd.crc.safa.test.features.notifications.documents;

import static org.assertj.core.api.AssertionsForInterfaceTypes.assertThat;

import java.util.List;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.notifications.entities.NotificationAction;
import edu.nd.crc.safa.test.requests.SafaRequest;

public class TestDeleteDocumentNotification extends AbstractDocumentNotificationTest {

    @Override
    public void setupTestResources() throws Exception {
        super.setupTestResources();
        this.createDocumentAndVerifyMessage();
    }

    @Override
    protected void performAction() throws Exception {
        SafaRequest
            .withRoute(AppRoutes.Documents.DELETE_DOCUMENT_BY_ID)
            .withDocument(documentConstants.document)
            .deleteWithJsonObject();
    }

    @Override
    protected void verifyShareeMessage(List<EntityChangeMessage> messages) {
        assertThat(messages).hasSize(1);
        EntityChangeMessage message = messages.get(0);
        this.changeMessageVerifies.verifyDocumentChange(
            message,
            this.documentId,
            NotificationAction.DELETE
        );
        this.changeMessageVerifies.verifyUpdateLayout(message, false);
    }
}
