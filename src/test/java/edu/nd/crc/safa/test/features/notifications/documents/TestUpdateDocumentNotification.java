package edu.nd.crc.safa.test.features.notifications.documents;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.List;

import edu.nd.crc.safa.config.AppRoutes;
import edu.nd.crc.safa.features.notifications.entities.EntityChangeMessage;
import edu.nd.crc.safa.features.notifications.entities.NotificationAction;
import edu.nd.crc.safa.test.requests.SafaRequest;

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
    protected void verifyShareeMessages(List<EntityChangeMessage> messages) {
        assertEquals(1, messages.size());
        EntityChangeMessage message = messages.get(0);
        this.messageVerificationService.verifyDocumentChange(
            message,
            this.documentId,
            NotificationAction.UPDATE
        );
        this.messageVerificationService.verifyUpdateLayout(message, false);
    }
}
