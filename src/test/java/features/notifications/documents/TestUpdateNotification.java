package features.notifications.documents;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;

import requests.SafaRequest;

public class TestUpdateNotification extends AbstractDocumentNotificationTest {

    @Override
    public void createShareeAccountAndShareProject() throws Exception {
        super.createShareeAccountAndShareProject();
        this.createDocument();
        EntityChangeMessage entityChangeMessage = this.notificationTestService.getNextMessage(Sharee.email);
        this.verifyShareeMessage(entityChangeMessage);
    }

    @Override
    protected void performAction() throws Exception {
        constants.document.setName("new-name");
        SafaRequest
            .withRoute(AppRoutes.Documents.CREATE_OR_UPDATE_DOCUMENT)
            .withVersion(projectVersion)
            .postWithJsonObject(constants.document);
    }
}
