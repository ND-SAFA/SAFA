package features.notifications.documents;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.notifications.entities.Change;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;

import requests.SafaRequest;

public class TestDeleteNotification extends AbstractDocumentNotificationTest {

    @Override
    public void createShareeAccountAndShareProject() throws Exception {
        super.createShareeAccountAndShareProject();
        this.createDocument();
        EntityChangeMessage entityChangeMessage = this.notificationTestService.getNextMessage(Sharee.email);
        super.verifyShareeMessage(entityChangeMessage);
    }

    @Override
    protected void performAction() throws Exception {
        SafaRequest
            .withRoute(AppRoutes.Documents.DELETE_DOCUMENT_BY_ID)
            .withDocument(constants.document)
            .deleteWithJsonObject();
    }

    @Override
    public void verifyShareeMessage(EntityChangeMessage message) {
        super.verifyDocumentMessage(message, Change.Action.DELETE);
    }
}
