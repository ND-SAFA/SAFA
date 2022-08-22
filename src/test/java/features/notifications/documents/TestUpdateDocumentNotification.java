package features.notifications.documents;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;

import requests.SafaRequest;

public class TestUpdateDocumentNotification extends AbstractDocumentNotificationTest {

    @Override
    public void setupTestResources() throws Exception {
        super.setupTestResources();
        this.createDocumentAndVerifyMessage();
    }

    @Override
    protected void performAction() throws Exception {
        documentConstants.document.setName("new-name");
        SafaRequest
            .withRoute(AppRoutes.Documents.CREATE_OR_UPDATE_DOCUMENT)
            .withVersion(projectVersion)
            .postWithJsonObject(documentConstants.document);
    }

    @Override
    protected void verifyShareeMessage(EntityChangeMessage message) {
        this.changeMessageVerifies.verifyDocumentChange(
            message,
            this.documentId,
            Change.Action.UPDATE
        );
        this.changeMessageVerifies.verifyUpdateLayout(message, false);
    }
}
