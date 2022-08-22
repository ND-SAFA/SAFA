package features.notifications.documents;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;

import requests.SafaRequest;

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
    protected void verifyShareeMessage(EntityChangeMessage message) {
        this.changeMessageVerifies.verifyDocumentChange(
            message,
            this.documentId,
            Change.Action.DELETE
        );
        this.changeMessageVerifies.verifyUpdateLayout(message, false);
    }
}
